from abc import ABC, abstractmethod
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PessoaFisicaRepositoryInterface(ABC):

    @abstractmethod
    def create_pessoa_fisica(  # pylint: disable=too-many-arguments, too-many-positional-arguments
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
    def get_pessoa_fisica(self, pessoa_fisica_id: int) -> PessoaFisicaTable:
        pass

    @abstractmethod
    def sacar(self, pessoa_fisica_id: int, valor: float) -> tuple[bool, str]:
        pass

    @abstractmethod
    def extrato(self, pessoa_fisica_id: int) -> tuple[bool, str]:
        pass
