from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class PessoaJuridicaRepositoryInterface(ABC):

    @abstractmethod
    def create_pessoa_juridica(  # pylint: disable=too-many-arguments, too-many-positional-arguments
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
    def read_pessoa_juridica(self, pessoa_juridica_id: int) -> PessoaJuridicaTable:
        pass

    @abstractmethod
    def sacar(self, pessoa_juridica_id: int, valor: float) -> tuple[bool, str]:
        pass

    @abstractmethod
    def extrato(self, pessoa_juridica_id: int) -> tuple[bool, str]:
        pass
