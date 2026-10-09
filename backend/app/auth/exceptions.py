from fastapi import HTTPException, status

class AuthException(Exception):
    """Base exception for authentication and authorization errors."""
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationFailed(AuthException):
    """Raised when authentication credentials are invalid."""
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class AuthorizationDenied(AuthException):
    """Raised when a user is authenticated but lacks required permissions."""
    def __init__(self, message: str = "You do not have permission to access this resource"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)

class InvalidToken(AuthException):
    """Raised when a JWT is malformed or signature is invalid."""
    def __init__(self, message: str = "Invalid authentication token"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class ExpiredToken(AuthException):
    """Raised when a JWT has expired."""
    def __init__(self, message: str = "Authentication token has expired"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class InactiveUser(AuthException):
    """Raised when a user account is disabled."""
    def __init__(self, message: str = "User account is inactive"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class UserAlreadyExists(AuthException):
    """Raised when trying to register an email that is already taken."""
    def __init__(self, message: str = "A user with this email already exists"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)
