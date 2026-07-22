"""
Email Service

Builds the actual email content (subject/body) for auth-related
emails and sends it through EmailClient. Kept separate from
EmailClient so the SMTP transport stays reusable for any future
email type.
"""

import logging
from datetime import datetime

from app.core.config import settings
from app.core.email import EmailClientError, email_client

logger = logging.getLogger("smart_hire.email_service")


class EmailService:
    """
    Sends transactional emails for the auth flow.
    """

    def send_otp_email(
        self,
        to_email: str,
        first_name: str,
        otp_code: str,
        purpose_label: str,
    ) -> bool:
        """
        Send an OTP code email. Returns True if the email was
        sent, False if sending failed (the failure is logged
        with full detail either way - this never raises so it
        can't take down the calling request).
        """

        subject = f"Your Smart Hire {purpose_label} code"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #2563eb;">Smart Hire</h2>
            <p>Hi {first_name},</p>
            <p>Your {purpose_label.lower()} code is:</p>
            <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px;
                      background: #f3f4f6; padding: 16px; text-align: center;
                      border-radius: 8px;">
                {otp_code}
            </p>
            <p>This code expires in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
            <p>If you didn't request this, you can safely ignore this email.</p>
            <p style="color: #6b7280; font-size: 12px; margin-top: 32px;">
                &copy; Smart Hire
            </p>
        </div>
        """

        text_body = (
            f"Hi {first_name},\n\n"
            f"Your {purpose_label.lower()} code is: {otp_code}\n"
            f"This code expires in {settings.OTP_EXPIRY_MINUTES} minutes.\n\n"
            "If you didn't request this, you can safely ignore this email."
        )

        try:
            email_client.send_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )
            return True

        except EmailClientError as e:
            # Already logged with full detail inside EmailClient.
            # Don't let an email outage break registration/login.
            logger.error(
                "send_otp_email failed for %s (purpose=%s): %s",
                to_email,
                purpose_label,
                e,
            )
            return False

    def send_welcome_email(
        self,
        to_email: str,
        first_name: str,
    ) -> bool:
        """
        Send a welcome email after successful registration and email verification.
        """
        subject = "Welcome to Smart Hire!"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1>Welcome to Smart Hire!</h1>
            </div>
            <div style="padding: 20px; background: #f9fafb;">
                <p>Hi {first_name},</p>
                <p>Your account has been successfully created and verified. You're all set to get started!</p>
                <p><strong>What you can do now:</strong></p>
                <ul>
                    <li>Complete your profile information</li>
                    <li>Browse available services</li>
                    <li>Connect with service providers or customers</li>
                </ul>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p style="color: #6b7280; font-size: 12px; margin-top: 32px;">
                    &copy; Smart Hire - Connecting Service Providers with Customers
                </p>
            </div>
        </div>
        """

        text_body = (
            f"Hi {first_name},\n\n"
            "Welcome to Smart Hire!\n\n"
            "Your account has been successfully created and verified. You're all set to get started!\n\n"
            "What you can do now:\n"
            "- Complete your profile information\n"
            "- Browse available services\n"
            "- Connect with service providers or customers\n\n"
            "If you have any questions, feel free to reach out to our support team.\n\n"
            "&copy; Smart Hire"
        )

        try:
            email_client.send_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )
            logger.info("Welcome email sent to %s", to_email)
            return True
        except EmailClientError as e:
            logger.error("Failed to send welcome email to %s: %s", to_email, e)
            return False

    def send_login_notification(
        self,
        to_email: str,
        first_name: str,
        login_time: datetime,
        ip_address: str,
        browser: str | None,
        operating_system: str | None,
        device: str | None,
        location: str | None,
        is_new_device: bool = False,
    ) -> bool:
        """
        Send a login notification email after successful authentication.
        """
        subject = "New login to your Smart Hire account"
        
        device_info = f"{browser or 'Unknown Browser'} on {operating_system or 'Unknown OS'}"
        if device:
            device_info = f"{device} ({device_info})"

        warning_message = ""
        if is_new_device:
            warning_message = """
            <div style="background: #fef3c7; border: 1px solid #fcd34d; padding: 16px; margin: 20px 0; border-radius: 8px;">
                <p style="color: #92400e; margin: 0;">
                    <strong>⚠️ New Device:</strong> This login was detected from a new device. 
                    If this wasn't you, please secure your account immediately.
                </p>
            </div>
            """

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1>Login Notification</h1>
            </div>
            <div style="padding: 20px; background: #f9fafb;">
                <p>Hi {first_name},</p>
                <p>Your Smart Hire account was just logged into. Here are the details:</p>
                
                <div style="background: white; border: 1px solid #e5e7eb; padding: 16px; margin: 20px 0; border-radius: 8px;">
                    <p><strong>Login Details:</strong></p>
                    <p style="margin: 8px 0;">
                        <strong>Time:</strong> {login_time.strftime('%Y-%m-%d %H:%M:%S %Z')}
                    </p>
                    <p style="margin: 8px 0;">
                        <strong>IP Address:</strong> {ip_address or 'Unknown'}
                    </p>
                    <p style="margin: 8px 0;">
                        <strong>Device:</strong> {device_info}
                    </p>
                    {f'<p style="margin: 8px 0;"><strong>Location:</strong> {location}</p>' if location else ''}
                </div>

                {warning_message}

                <p style="color: #666; font-size: 14px;">
                    If this wasn't you, please <strong>change your password immediately</strong> and 
                    <a href="https://smarthire.example.com/security" style="color: #2563eb;">review your account security settings</a>.
                </p>
                
                <p style="color: #6b7280; font-size: 12px; margin-top: 32px;">
                    &copy; Smart Hire - Your account security is our priority
                </p>
            </div>
        </div>
        """

        text_body = (
            f"Hi {first_name},\n\n"
            "Your Smart Hire account was just logged into. Here are the details:\n\n"
            f"Time: {login_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"IP Address: {ip_address or 'Unknown'}\n"
            f"Device: {device_info}\n"
            f"{f'Location: {location}' if location else ''}\n\n"
        )

        if is_new_device:
            text_body += (
                "⚠️  This login was detected from a new device.\n"
                "If this wasn't you, please secure your account immediately.\n\n"
            )

        text_body += (
            "If this wasn't you, please change your password immediately and "
            "review your account security settings.\n\n"
            "&copy; Smart Hire"
        )

        try:
            email_client.send_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )
            logger.info("Login notification sent to %s", to_email)
            return True
        except EmailClientError as e:
            logger.error("Failed to send login notification to %s: %s", to_email, e)
            return False

    def send_suspicious_activity_alert(
        self,
        to_email: str,
        first_name: str,
        activity_type: str,
        details: str,
    ) -> bool:
        """
        Send a suspicious activity alert email.
        """
        subject = "Suspicious Activity Alert - Smart Hire"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #dc2626; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                <h1>⚠️  Suspicious Activity Detected</h1>
            </div>
            <div style="padding: 20px; background: #fef2f2;">
                <p>Hi {first_name},</p>
                <p>We detected suspicious activity on your Smart Hire account.</p>
                
                <div style="background: white; border: 2px solid #dc2626; padding: 16px; margin: 20px 0; border-radius: 8px;">
                    <p><strong>Activity Type:</strong> {activity_type}</p>
                    <p><strong>Details:</strong></p>
                    <p>{details}</p>
                </div>

                <p style="color: #666; font-size: 14px;">
                    <strong>What to do:</strong>
                </p>
                <ul style="color: #666;">
                    <li>If this was you, you can safely ignore this email.</li>
                    <li>If this wasn't you, <strong>change your password immediately</strong>.</li>
                    <li>Review your login history and revoke access to untrusted devices.</li>
                </ul>
                
                <p style="color: #6b7280; font-size: 12px; margin-top: 32px;">
                    &copy; Smart Hire - We take your security seriously
                </p>
            </div>
        </div>
        """

        text_body = (
            f"Hi {first_name},\n\n"
            "We detected suspicious activity on your Smart Hire account.\n\n"
            f"Activity Type: {activity_type}\n"
            f"Details: {details}\n\n"
            "What to do:\n"
            "- If this was you, you can safely ignore this email.\n"
            "- If this wasn't you, change your password immediately.\n"
            "- Review your login history and revoke access to untrusted devices.\n\n"
            "&copy; Smart Hire"
        )

        try:
            email_client.send_email(
                to_email=to_email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
            )
            logger.info("Suspicious activity alert sent to %s", to_email)
            return True
        except EmailClientError as e:
            logger.error("Failed to send suspicious activity alert to %s: %s", to_email, e)
            return False


email_service = EmailService()
