from enum import Enum
from typing import Optional


class HTTPStatusCode(Enum):
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_400_BAD_REQUEST = 400
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_408_REQUEST_TIMEOUT = 408
    HTTP_409_CONFLICT = 409
    HTTP_422_UNPROCESSABLE_ENTITY = 422
    HTTP_429_TOO_MANY_REQUESTS = 429
    HTTP_500_INTERNAL_SERVER_ERROR = 500


class AbstractException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
    ) -> None:
        self._status_code = status_code
        self._detail = detail

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return (
            f"{class_name}(status_code={self._status_code!r}, detail={self._detail!r})"
        )

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def detail(self) -> str:
        return self._detail
