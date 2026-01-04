from typing import Optional
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.models.sqlite.repositories.base_repository import BaseRepository
from src.models.sqlite.interfaces.pessoa_fisica_repository import (
    PessoaFisicaRepositoryInterface
)
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable


class PessoaFisicaRepository(BaseRepository[PessoaFisicaTable], PessoaFisicaRepositoryInterface):
    LIMITE_SAQUE_DIARIO = 1000.0

    def __init__(self, db_connection) -> None:
        super().__init__(db_connection, PessoaFisicaTable)

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
        pessoa_fisica_data = PessoaFisicaTable(
            renda_mensal=renda_mensal,
            idade=idade,
            nome_completo=nome_completo,
            celular=celular,
            email=email,
            categoria=categoria,
            saldo=saldo
        )
        self._create_entity(pessoa_fisica_data)

    def get_pessoa_fisica(self, pessoa_fisica_id: int) -> Optional[PessoaFisicaTable]:
        return self._get_by_id(pessoa_fisica_id)

    def sacar(self, pessoa_fisica_id: int, valor: float) -> tuple[bool, str]:
        return self._sacar_generic(
            pessoa_fisica_id,
            valor,
            self.LIMITE_SAQUE_DIARIO,
            "PF",
            "Pessoa física"
        )

    def extrato(self, pessoa_fisica_id: int) -> tuple[bool, str]:
        pessoa_fisica = self._get_by_id(pessoa_fisica_id)

        if pessoa_fisica is None:
            raise HttpNotFoundError(f"Pessoa física com ID {pessoa_fisica_id} não encontrada")

        return True, f"Extrato - Saldo atual: R${pessoa_fisica.saldo:.2f}"
