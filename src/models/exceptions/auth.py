from archipy.models.errors import (
    InvalidTokenError,
    NotFoundError,
    PermissionDeniedError,
    TokenExpiredError,
    UnauthenticatedError,
)


class InvalidCredentialsError(UnauthenticatedError):
    """Error raised when credentials are invalid."""

    def __init__(self) -> None:
        super().__init__()


class AuthTokenExpiredError(TokenExpiredError):
    """Error raised when JWT token has expired."""

    def __init__(self) -> None:
        super().__init__()


class AuthInvalidTokenError(InvalidTokenError):
    """Error raised when JWT token is invalid."""

    def __init__(self) -> None:
        super().__init__()


class InvalidSchemeError(UnauthenticatedError):
    """Error raised when authentication scheme is not Bearer."""

    def __init__(self) -> None:
        super().__init__()


class MissingCredentialsError(UnauthenticatedError):
    """Error raised when no credentials are provided."""

    def __init__(self) -> None:
        super().__init__()


class AuthPermissionDeniedError(PermissionDeniedError):
    """Error raised when user doesn't have required permissions."""

    def __init__(self) -> None:
        super().__init__()


class AuthUserNotFoundError(NotFoundError):
    """Error raised when the user is not found."""

    def __init__(self) -> None:
        super().__init__()
