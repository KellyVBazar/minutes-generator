import json

from typing import Dict, Any
from aws_lambda_typing import context as context_

from common.logger_handler import logger
from common.constants import HTTPStatusCodes
from common.utils import set_lambda_response

from get_pipefy import TermsGeneration

def lambda_handler(event: Dict[str, Any], _context: context_.Context) -> Dict[str, Any]:
    logger.info(f"Recebido evento: {event}")
    try:
        body = json.loads(event.get("body", "{}"))
        envelope_id = TermsGeneration().generate(body['card_id'])
        return set_lambda_response(HTTPStatusCodes.CREATED.value,
                                   {"result": f"Documentos gerados e criado envelope: {envelope_id}"})
    except KeyError as error:
        message = f'Evento recebido não contén chave esperada: {error}'
        logger.error(message)
        return set_lambda_response(HTTPStatusCodes.UNPROCESSABLE_ENTITY.value, {"error": message})
    except Exception as generic_error:
        message = f'Erro inesperado: {generic_error}'
        logger.error(message)
        return set_lambda_response(HTTPStatusCodes.INTERNAL_SERVER_ERROR.value, {"error": message})

if __name__ == "__main__":  # pragma: no cover
    test_event = {
        "card_id": "1167217322"
    }
    response = lambda_handler({"body": json.dumps(test_event)}, None)
    print(response)