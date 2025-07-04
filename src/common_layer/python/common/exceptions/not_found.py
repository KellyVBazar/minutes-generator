from common.exceptions.abstract_exception import AbstractException, HTTPStatusCode


class NotFoundException(AbstractException):
    def __init__(self, detail: str = "Dado não encontrado."):
        super().__init__(HTTPStatusCode.HTTP_404_NOT_FOUND.value, detail=detail)
