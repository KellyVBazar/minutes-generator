from common.exceptions.abstract_exception import AbstractException, HTTPStatusCode


class InternalErrorException(AbstractException):
    def __init__(self, detail: str = "Internal Server Error."):
        super().__init__(HTTPStatusCode.HTTP_500_INTERNAL_SERVER_ERROR.value, detail=detail)
