from abc import ABC
from typing import Dict, Any, Tuple, List


class BaseController(ABC):
    """Classe base para controladores com métodos auxiliares comuns."""

    @staticmethod
    def validar_dados_obrigatorios(dados: Dict[str, Any], campos: List[str]) -> Tuple[bool, str]:
        for campo in campos:
            if campo not in dados or not dados[campo]:
                return False, f"Campo '{campo}' é obrigatório"
        return True, ""

    @staticmethod
    def formatar_resposta_sucesso(mensagem: str, detalhes: str = "") -> Dict[str, Any]:
        resposta = {
            "success": True,
            "message": mensagem
        }
        if detalhes:
            resposta["details"] = detalhes
        return resposta

    @staticmethod
    def formatar_resposta_erro(mensagem: str) -> Dict[str, Any]:
        return {
            "success": False,
            "message": mensagem
        }
