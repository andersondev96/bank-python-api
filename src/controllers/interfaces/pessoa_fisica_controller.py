from typing import Optional, Tuple
from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PessoaFisicaControllerInterface(ABC):

    @abstractmethod
    def criar(self, dados: dict) -> None:
        pass

    @abstractmethod
    def buscar(self, pessoa_id: int) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def sacar(self, pessoa_id: int, valor: float) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def extrato(self, pessoa_id: int) -> Tuple[bool, str]:
        pass
