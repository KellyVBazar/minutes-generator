from common.exceptions.abstract_exception import AbstractException, HTTPStatusCode


class UnprocessableException(AbstractException):
    def __init__(self, detail: str = "Dados em formato inválido"):
        super().__init__(HTTPStatusCode.HTTP_422_UNPROCESSABLE_ENTITY.value, detail=detail)
