"""
Custom Exceptions

Defines application-specific exceptions.
"""


class AppException(Exception):
    """
    Base application exception.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# =====================================================
# Authentication
# =====================================================

class AuthenticationException(AppException):
    """
    Authentication failed.
    """

    def __init__(
        self,
        message: str = "Authentication failed.",
    ):
        super().__init__(
            message,
            status_code=401,
        )


class AuthorizationException(AppException):
    """
    Permission denied.
    """

    def __init__(
        self,
        message: str = "Permission denied.",
    ):
        super().__init__(
            message,
            status_code=403,
        )


# =====================================================
# Resources
# =====================================================

class NotFoundException(AppException):
    """
    Resource not found.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
    ):
        super().__init__(
            message,
            status_code=404,
        )


class ValidationException(AppException):
    """
    Validation failed.
    """

    def __init__(
        self,
        message: str = "Validation failed.",
    ):
        super().__init__(
            message,
            status_code=400,
        )


class ConflictException(AppException):
    """
    Resource conflict.
    """

    def __init__(
        self,
        message: str = "Resource already exists.",
    ):
        super().__init__(
            message,
            status_code=409,
        )


class DatabaseException(AppException):
    """
    Database operation failed.
    """

    def __init__(
        self,
        message: str = "Database operation failed.",
    ):
        super().__init__(
            message,
            status_code=500,
        )
        