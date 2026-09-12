from typing import Any


class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400, details: Any = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(message, code, 404)


class ConflictError(AppError):
    def __init__(self, message: str, code: str = "CONFLICT"):
        super().__init__(message, code, 409)


class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid authentication credentials"):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)


class AuthorizationError(AppError):
    def __init__(self, message: str = "You do not have access to this resource"):
        super().__init__(message, "FORBIDDEN", 403)


class ExternalServiceError(AppError):
    def __init__(self, service: str, message: str | None = None):
        super().__init__(message or f"{service} is temporarily unavailable", f"{service.upper()}_SERVICE_ERROR", 503)
