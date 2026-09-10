class AuthenticationError(Exception):
    """Raised when authentication fails."""


class AuthorizationError(Exception):
    """Raised when an authenticated user lacks permission."""


class InvalidTokenError(AuthenticationError):
    """Raised when a JWT is invalid or expired."""


class UserNotFoundError(AuthenticationError):
    """Raised when an authenticated user no longer exists."""
