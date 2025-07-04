import os
import json
import requests

from common.aws.secret_manager import SecretManager
from common.exceptions import InternalErrorException
from common.logger_handler import logger


class ClickSignService:
    ENVELOPE_ID = "<envelope_id>"

    def __init__(self) -> None:
        self.__base_url = os.environ['CLICKSIGN_URL']
        secret_tokens = SecretManager().get_secret_value(os.environ["SECRET_TOKENS_NAME"])

        self.__headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'Authorization': secret_tokens['clicksign_api_key']
        }
        self.__envelope_endpoint = f'{self.__base_url}/api/v3/envelopes'
        self.__signers_endpoint = f'{self.__base_url}/api/v3/envelopes/<envelope_id>/signers'

    def create_envelope(self, client_name: str, precatorio_number: str) -> str:
        body = {
            "data": {
                "type": "envelopes",
                "attributes": {
                    "name": f'{client_name} - {precatorio_number}',
                    "locale": "pt-BR",
                    "auto_close": True,
                    "remind_interval": "3",
                    "block_after_refusal": True
                }
            }
        }

        response = requests.post(self.__envelope_endpoint, json=body, headers=self.__headers)

        if response.status_code != 201:
            message = f'Requisição para criar envelope no clicksign falhou: {response.json()}'
            logger.error(message)
            raise InternalErrorException(message)

        return response.json().get('data', {}).get('id')

    def create_signers(self, signer_data: dict, envelope_id: str) -> str:
        body = {
            "data": {
                "type": "signers",
                "attributes": {
                    "name": signer_data["name"],
                    "birthday": signer_data["birthday"],
                    "email": signer_data["email"],
                    "has_documentation": signer_data["has_documentation"],
                    "documentation": signer_data["documentation"],
                    "refusable": signer_data["refusable"],
                    "communicate_events": signer_data["communicate_events"]
                }
            }
        }

        response = requests.post(
            self.__signers_endpoint.replace(self.ENVELOPE_ID, envelope_id), json=body, headers=self.__headers)

        if response.status_code != 201:
            message = f'Requisição para criar signatário no clicksign falhou: {response.json()}'
            logger.error(message)
            raise InternalErrorException(message)

        return response.json().get('data', {}).get('id')