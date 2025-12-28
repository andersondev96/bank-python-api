from abc import ABC, abstractmethod
from typing import Optional
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class PessoaJuridicaRepositoryInterface(ABC):
    @abstractmethod
    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def create_pessoa_juridica(
        self,
        faturamento: float,
        idade: int,
        nome_fantasia: str,
        celular: str,
        email_corporativo: str,
        categoria: str,
        saldo: float
    ) -> None:
        pass

    @abstractmethod
    def read_pessoa_juridica(self, pessoa_juridica_id: int) -> Optional[PessoaJuridicaTable]:
        pass

    @abstractmethod
    def sacar(self, pessoa_juridica_id: int, valor: float) -> tuple[bool, str]:
        pass

    @abstractmethod
    def extrato(self, pessoa_juridica_id: int) -> tuple[bool, str]:
        pass
