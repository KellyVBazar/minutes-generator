import json

from common.logger_handler import logger
from typing import Any, Dict


def set_lambda_response(status_code: int, body: Any) -> Dict[str, Any]:
    response = {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }

    logger.info(f"Response: {response}")
    return response
