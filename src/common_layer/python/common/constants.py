from enum import Enum


class HTTPStatusCodes(Enum):
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
