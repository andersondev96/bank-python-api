from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.interfaces.pessoa_juridica_repository import (
    PessoaJuridicaRepositoryInterface
)
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable

class PessoaJuridicaRepository(PessoaJuridicaRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection

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
        with self.db_connection as database:
            try:
                pessoa_juridica_data = PessoaJuridicaTable(
                    faturamento=faturamento,
                    idade=idade,
                    nome_fantasia=nome_fantasia,
                    celular=celular,
                    email_corporativo=email_corporativo,
                    categoria=categoria,
                    saldo=saldo
                )
                database.session.add(pessoa_juridica_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def read_pessoa_juridica(self, pessoa_juridica_id: int) -> PessoaJuridicaTable:
        with self.db_connection as database:
            try:
                pessoa_juridica = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == pessoa_juridica_id)
                    .one()
                )
                return pessoa_juridica
            except NoResultFound:
                return None

    def sacar(self, pessoa_juridica_id: int, valor: float) -> tuple[bool, str]:  # pylint: disable=arguments-differ
        with self.db_connection as database:
            try:
                pessoa_juridica = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == pessoa_juridica_id)
                    .one()
                )

                limite_saque_pj = 5000.0

                if valor <= 0:
                    return False, "Valor do saque deve ser Positivo"

                if valor > pessoa_juridica.saldo:
                    return False, f"Saldo insuficiente. Saldo atual: R${pessoa_juridica.saldo:.2f}"

                if valor > limite_saque_pj:
                    return False, f"Saque excede o limite diário para PF: R${limite_saque_pj:.2f}"


                pessoa_juridica.saldo -= valor
                database.session.commit()

                return True, (
                    f"Saque de R${valor:.2f} realizado com sucesso. "
                    f"Novo saldo: R${pessoa_juridica.saldo:.2f}"
                )
            except NoResultFound:
                return False, f"Pessoa física com ID {pessoa_juridica_id} não encontrada"
            except Exception as exception:
                database.session.rollback()
                raise exception

    def extrato(self, pessoa_juridica_id: int) -> tuple[bool, str]:  # pylint: disable=arguments-renamed
        with self.db_connection as database:
            try:
                pessoa_juridica = (
                    database.session.query(PessoaJuridicaTable)
                    .filter(PessoaJuridicaTable.id == pessoa_juridica_id)
                    .one()
                )

                return True, f"Extrato - Saldo atual: R${pessoa_juridica.saldo:.2f}"
            except NoResultFound:
                return False, f"Pessoa física com ID {pessoa_juridica_id} não encontrada"
