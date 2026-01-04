from typing import Optional
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.models.sqlite.repositories.base_repository import BaseRepository
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface
)
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class PessoaJuridicaRepository(
    BaseRepository[PessoaJuridicaTable],
    PessoaJuridicaRepositoryInterface
):

    LIMITE_SAQUE_DIARIO = 5000.0

    def __init__(self, db_connection) -> None:
        super().__init__(db_connection, PessoaJuridicaTable)

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
        """Cria uma nova pessoa jurídica no banco de dados."""
        pessoa_juridica_data = PessoaJuridicaTable(
            faturamento=faturamento,
            idade=idade,
            nome_fantasia=nome_fantasia,
            celular=celular,
            email_corporativo=email_corporativo,
            categoria=categoria,
            saldo=saldo
        )
        self._create_entity(pessoa_juridica_data)

    def read_pessoa_juridica(self, pessoa_juridica_id: int) -> Optional[PessoaJuridicaTable]:
        return self._get_by_id(pessoa_juridica_id)

    def sacar(self, pessoa_juridica_id: int, valor: float) -> tuple[bool, str]:
        return self._sacar_generic(
            pessoa_juridica_id,
            valor,
            self.LIMITE_SAQUE_DIARIO,
            "PJ",
            "Pessoa jurídica"
        )

    def extrato(self, pessoa_juridica_id: int) -> tuple[bool, str]:
        pessoa_juridica = self._get_by_id(pessoa_juridica_id)

        if pessoa_juridica is None:
            raise HttpNotFoundError(f"Pessoa jurídica com ID {pessoa_juridica_id} não encontrada")

        return True, f"Extrato - Saldo atual: R${pessoa_juridica.saldo:.2f}"
