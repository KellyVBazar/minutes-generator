import os
import re

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

    def __set_target_templates(self, phase_id: str) -> None:
        self.__target_templates = {key: value for key, value in self.__templates.items()
                                   if value['phase_id'] == phase_id}

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