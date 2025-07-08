import os
import requests

from common.aws.secret_manager import SecretManager
from common.exceptions import InternalErrorException
from common.logger_handler import logger


class PipefyService:
    def __init__(self) -> None:
        self.__base_url = os.environ['PIPEFY_URL']
        secret_tokens = SecretManager().get_secret_value(os.environ["SECRET_TOKENS_NAME"])

        self.__headers = {
            'Authorization': f'Bearer {secret_tokens["pipefy_token"]}',
            'Content-Type': 'application/json'
        }

    def post_query(self, query: str, variables: dict = None) -> dict:
        body = {'query': query}
        if variables:
            body["variables"] = variables

        try:
            response = requests.post(self.__base_url, json=body, headers=self.__headers)
            response.raise_for_status()
            content = response.json()
        except requests.RequestException as e:
            logger.error(f"Requisição ao Pipefy retornou erro {self.__base_url}: {e}")
            raise e

        if 'errors' in content or 'error' in content:
            message = f"Requisição ao Pipefy retornou erro {content}"
            logger.error(message)
            raise InternalErrorException(message)
        else:
            return content

    def get_card_fields(self, card_id: str) -> dict:
        query = '''
        query GetCardFields($cardId: ID!) {
          card(id: $cardId) {
            id
            title
            fields {
              name
              value
            }
            current_phase {
              id
              name
            }
          }
        }
        '''
        variables = {
            "cardId": card_id
        }
        return self.post_query(query, variables)