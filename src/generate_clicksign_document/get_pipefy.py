import os
import re

from collections import defaultdict
from datetime import datetime
from typing import Dict, List
from unidecode import unidecode

from common.external_services.pipefy import PipefyService
from common.external_services.clicksign import ClickSignService
from common.logger_handler import logger

class TermsGeneration:
    def __init__(self) -> None:
        self.__pipefy_service = PipefyService()
        self.__clicksign_service = ClickSignService()

        self.__templates = {
            "Termo de Cessao": {
                "key": os.getenv("PRECA_CESSION_TERM_KEY"),
                "phase_id": os.environ['CONTRACT_PHASE_ID']
            }
        }
        self.__target_templates = {}

    @staticmethod
    def __rename_pipefy_fields(field_name: str) -> str:
        field_name = unidecode(field_name).lower().strip()
        field_name = re.sub(r'\s+', ' ', field_name)
        field_name = re.sub(r'[^a-z\d\-_ ]', '', field_name).strip()
        field_name = field_name.replace(' ', '_').replace('-', '_')
        return re.sub(r'_+', '_', field_name)

    @staticmethod
    def __parse_birthday(birthday_str: str) -> str:
        """Converte data em formato brasileiro ou americano para ISO-8601."""
        for fmt in ("%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(birthday_str, fmt).date().strftime("%Y-%m-%d")
            except ValueError:
                pass
        raise ValueError(f"Data de aniversário em formato desconhecido: {birthday_str}")

    def __set_target_templates(self, phase_id: str) -> None:
        self.__target_templates = {key: value for key, value in self.__templates.items()
                                   if value['phase_id'] == phase_id}


    def __create_signers(self, client_name: str, client_cpf: str, client_email: str,
                         birthday: str, envelope_id: str) -> Dict[str, List[dict]]:
        signers = defaultdict(list)
        communicate_events = {
            "communicate_events": {
                "document_signed": "email",
                "signature_request": "email",
                "signature_reminder": "email"
            }
        }

        birthday_iso = self.__parse_birthday(birthday)
        client = {
            "name": client_name,
            "email": client_email,
            "has_documentation": True,
            "documentation": client_cpf,
            "birthday": birthday_iso,
            "refusable": False
        }
        client.update(**communicate_events)
        signer_id = self.__clicksign_service.create_signers(client, envelope_id)
        return {"signers": [{"signer_id": signer_id}]}


    def generate(self, card_id: str) -> str:
        result = self.__pipefy_service.get_card_fields(card_id)
        phase_id = result['data']['card']['current_phase']['id']

        self.__set_target_templates(phase_id)
        card_data = result['data']['card']['fields']
        card_data = {self.__rename_pipefy_fields(field['name']): field['value'] for field in card_data}
        logger.info(f"Dados obtidos do pipefy e padronizados: {card_data}")

        envelope_id = self.__clicksign_service.create_envelope(
            card_data["nome_completo_oficio"], card_data["numero_precatorio"])
        logger.info(f"Criado envelope no clicksign {envelope_id}")

        signers = self.__create_signers(
            card_data["nome_completo_oficio"], card_data["cpf_informado"],
            card_data["e_mail"], card_data["data_de_nascimento"], envelope_id)
        logger.info(f"Criados signatários no clicksign: {signers}")

        return envelope_id