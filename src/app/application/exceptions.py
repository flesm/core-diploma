from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class BadRequestException(AppException):
    def __init__(self, detail: str) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)
