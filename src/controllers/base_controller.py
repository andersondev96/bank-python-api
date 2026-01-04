from abc import ABC
from typing import Dict, Any, Tuple, List, Union


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
    def formatar_resposta_erro(erro: Union[str, Exception]) -> Dict[str, Any]:
        mensagem = getattr(erro, "message", str(erro))
        return {
            "success": False,
            "message": mensagem
        }
