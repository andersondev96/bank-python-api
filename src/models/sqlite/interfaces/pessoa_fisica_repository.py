from abc import ABC, abstractmethod
from typing import Optional
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable


class PessoaFisicaRepositoryInterface(ABC):
    @abstractmethod
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def create_pessoa_fisica(
        self,
        renda_mensal: float,
        idade: int,
        nome_completo: str,
        celular: str,
        email: str,
        categoria: str,
        saldo: float
    ) -> None:
        pass

    @abstractmethod
    def get_pessoa_fisica(self, pessoa_fisica_id: int) -> Optional[PessoaFisicaTable]:
        pass

    @abstractmethod
    def sacar(self, pessoa_fisica_id: int, valor: float) -> tuple[bool, str]:
        pass

    @abstractmethod
    def extrato(self, pessoa_fisica_id: int) -> tuple[bool, str]:
        pass
