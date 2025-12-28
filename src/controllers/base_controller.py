from abc import ABC
from typing import Dict, Any, Tuple


class BaseController(ABC):
    @staticmethod
    def validar_dados_obrigatorios(dados: Dict[str, Any], campos: list) -> Tuple[bool, str]:
        for campo in campos:
            if campo not in dados or not dados[campo]:
                return False, f"Campo '{campo}' é obrigatório"
        return True, ""

    @staticmethod
    def formatar_resposta_sucesso(operacao: str, detalhes: str = "") -> Dict[str, Any]:
        return {
            "success": True,
            "message": f"{operacao} realizado com sucesso",
            "details": detalhes
        }

    @staticmethod
    def formatar_resposta_erro(mensagem: str) -> Dict[str, Any]:
        return {
            "success": False,
            "message": mensagem
        }
