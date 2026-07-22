"""
Email Client

Low-level SMTP client responsible only for opening a
connection to the mail server, authenticating, and sending
a single message. Business logic (what the email says, when
it's sent) lives in app/services/email_service.py.

--------------------------------------------------------------
WHY "SMTPServerDisconnected: please run connect() first"
HAPPENS (root cause, for reference)
--------------------------------------------------------------
Port 465 and port 587 use two different, incompatible
handshakes:

  - Port 465 ("implicit TLS"): the TLS handshake happens the
    INSTANT the socket opens. The client must use
    smtplib.SMTP_SSL(...), which wraps the socket in TLS
    before speaking SMTP at all.

  - Port 587 ("explicit TLS" / STARTTLS): the client connects
    in plain text with smtplib.SMTP(...), says EHLO, then
    sends a STARTTLS command to upgrade the existing
    connection to TLS.

If you open a *plain* smtplib.SMTP(host, 465) connection
(i.e. the port-465 + STARTTLS combination), Gmail accepts the
raw TCP connection but refuses to speak plaintext SMTP on that
port and closes the socket almost immediately. The client
doesn't find out until the next command - typically
server.login(...) - at which point smtplib finds the socket
already closed and raises exactly:

    smtplib.SMTPServerDisconnected: please run connect() first

The fix is simply to match the client class to the port:
SMTP_SSL for 465, SMTP + starttls() for 587. This client does
that automatically based on settings.SMTP_USE_SSL.
"""

import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

logger = logging.getLogger("smart_hire.email")


class EmailClientError(Exception):
    """
    Raised when an email genuinely fails to send, after
    logging the real underlying SMTP error.
    """


class EmailClient:
    """
    Sends a single email over Gmail SMTP (or any SMTP server
    configured the same way).
    """

    def __init__(self) -> None:
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USERNAME
        self.from_name = settings.SMTP_FROM_NAME
        self.use_ssl = settings.SMTP_USE_SSL

    def _validate_config(self) -> None:
        missing = []

        if not self.host:
            missing.append("SMTP_HOST")
        if not self.port:
            missing.append("SMTP_PORT")
        if not self.username:
            missing.append("SMTP_USERNAME")
        if not self.password:
            missing.append("SMTP_PASSWORD")
        if not self.from_email:
            missing.append("SMTP_FROM_EMAIL")

        if missing:
            message = (
                "Email is not configured - missing: "
                + ", ".join(missing)
                + ". Set these in backend/.env."
            )
            logger.error(message)
            raise EmailClientError(message)

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
    ) -> None:
        """
        Send one email. Raises EmailClientError with a clear
        message if it fails - the real smtplib exception is
        always logged first so the actual cause is visible,
        not swallowed.
        """

        self._validate_config()

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email

        if text_body:
            message.attach(MIMEText(text_body, "plain"))

        message.attach(MIMEText(html_body, "html"))

        try:
            if self.use_ssl:
                self._send_via_ssl(to_email, message)
            else:
                self._send_via_starttls(to_email, message)

            logger.info(
                "Email sent successfully: to=%s subject=%r",
                to_email,
                subject,
            )

        except smtplib.SMTPAuthenticationError as e:
            logger.error(
                "SMTP authentication failed for %s on %s:%s - %s. "
                "This almost always means SMTP_PASSWORD is your "
                "normal Gmail password instead of a 16-character "
                "App Password, or 2-Step Verification isn't "
                "enabled on the Google account.",
                self.username,
                self.host,
                self.port,
                e,
            )
            raise EmailClientError(
                "SMTP authentication failed. Verify SMTP_USERNAME "
                "and SMTP_PASSWORD (must be a Gmail App Password)."
            ) from e

        except smtplib.SMTPServerDisconnected as e:
            logger.error(
                "SMTP server disconnected unexpectedly while "
                "talking to %s:%s (use_ssl=%s) - %s. This is "
                "almost always a port/handshake mismatch: use "
                "port 465 with SMTP_USE_SSL=True, or port 587 "
                "with SMTP_USE_SSL=False.",
                self.host,
                self.port,
                self.use_ssl,
                e,
            )
            raise EmailClientError(
                "The mail server disconnected unexpectedly. Check "
                "that SMTP_PORT and SMTP_USE_SSL match "
                "(465 -> True, 587 -> False)."
            ) from e

        except smtplib.SMTPConnectError as e:
            logger.error(
                "Could not connect to SMTP server %s:%s - %s. "
                "Check SMTP_HOST/SMTP_PORT and that outbound "
                "traffic on this port isn't blocked by a "
                "firewall or the network you're on.",
                self.host,
                self.port,
                e,
            )
            raise EmailClientError(
                "Could not connect to the mail server. Check "
                "SMTP_HOST, SMTP_PORT, and your network/firewall."
            ) from e

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(
                "SMTP server refused recipient %s - %s",
                to_email,
                e,
            )
            raise EmailClientError(
                f"The mail server rejected the recipient address "
                f"'{to_email}'."
            ) from e

        except (smtplib.SMTPException, ssl.SSLError, OSError) as e:
            logger.exception(
                "Unexpected error sending email to %s via %s:%s",
                to_email,
                self.host,
                self.port,
            )
            raise EmailClientError(
                f"Failed to send email: {e}"
            ) from e

    # =====================================================
    # Port 465 - implicit TLS
    # =====================================================

    def _send_via_ssl(self, to_email: str, message: MIMEMultipart) -> None:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            self.host,
            self.port,
            context=context,
            timeout=15,
        ) as server:
            server.login(self.username, self.password)
            server.sendmail(
                self.from_email,
                to_email,
                message.as_string(),
            )

    # =====================================================
    # Port 587 - explicit TLS (STARTTLS)
    # =====================================================

    def _send_via_starttls(self, to_email: str, message: MIMEMultipart) -> None:
        context = ssl.create_default_context()

        with smtplib.SMTP(self.host, self.port, timeout=15) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.username, self.password)
            server.sendmail(
                self.from_email,
                to_email,
                message.as_string(),
            )


email_client = EmailClient()
