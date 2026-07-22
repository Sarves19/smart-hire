"""Small in-process rate limiters for public authentication endpoints."""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status


class SlidingWindowRateLimiter:
    """Limit requests by client IP over a rolling window.

    Deployments running multiple workers should also enforce these limits at
    the reverse proxy or API gateway, where the counter can be shared.
    """

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def __call__(self, request: Request) -> None:
        # Robustly extract client IP: Starlette may provide a tuple or an object.
        client = getattr(request, "client", None)
        if client is None:
            client_ip = "unknown"
        else:
            # client can be a tuple (host, port) or an object with .host
            if hasattr(client, "host"):
                client_ip = client.host
            else:
                try:
                    client_ip = client[0]
                except Exception:
                    client_ip = "unknown"

        now = monotonic()
        with self._lock:
            # Use client IP only (not path) to allow shared limits per client
            timestamps = self._requests[client_ip]
            while timestamps and timestamps[0] <= now - self.window_seconds:
                timestamps.popleft()
            if len(timestamps) >= self.limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later.",
                    headers={"Retry-After": str(self.window_seconds)},
                )
            timestamps.append(now)


login_rate_limit = SlidingWindowRateLimiter(limit=10, window_seconds=60)
otp_rate_limit = SlidingWindowRateLimiter(limit=5, window_seconds=300)
