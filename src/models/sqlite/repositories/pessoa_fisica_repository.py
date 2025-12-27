from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.interfaces.pessoa_fisica_repository import PessoaFisicaRepositoryInterface
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

class PessoaFisicaRepository(PessoaFisicaRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.db_connection = db_connection


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
        with self.db_connection as database:
            try:
                pessoa_fisica_data = PessoaFisicaTable(
                    renda_mensal=renda_mensal,
                    idade=idade,
                    nome_completo=nome_completo,
                    celular=celular,
                    email=email,
                    categoria=categoria,
                    saldo=saldo
                )
                database.session.add(pessoa_fisica_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    def get_pessoa_fisica(self, pessoa_fisica_id: int) -> PessoaFisicaTable:
        with self.db_connection as database:
            try:
                pessoa_fisica = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_fisica_id)
                    .one()
                )
                return pessoa_fisica
            except NoResultFound:
                return None

    def sacar(self, pessoa_fisica_id: int, valor: float) -> tuple[bool, str]:
        with self.db_connection as database:
            try:
                pessoa_fisica = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_fisica_id)
                    .one()
                )

                limite_saque_pf = 1000.0

                if valor <= 0:
                    return False, "Valor do saque deve ser Positivo"

                if valor > pessoa_fisica.saldo:
                    return False, f"Saldo insuficiente. Saldo atual: R${pessoa_fisica.saldo:.2f}"

                if valor > limite_saque_pf:
                    return False, f"Saque excede o limite diário para PF: R${limite_saque_pf:.2f}"


                pessoa_fisica.saldo -= valor
                database.session.commit()

                return True, (
                    f"Saque de R${valor:.2f} realizado com sucesso. "
                    f"Novo saldo: R${pessoa_fisica.saldo:.2f}"
                )
            except NoResultFound:
                return False, f"Pessoa física com ID {pessoa_fisica_id} não encontrada"
            except Exception as exception:
                database.session.rollback()
                raise exception

    def extrato(self, pessoa_fisica_id: int) -> tuple[bool, str]:
        with self.db_connection as database:
            try:
                pessoa_fisica = (
                    database.session.query(PessoaFisicaTable)
                    .filter(PessoaFisicaTable.id == pessoa_fisica_id)
                    .one()
                )

                return True, f"Extrato - Saldo atual: R${pessoa_fisica.saldo:.2f}"
            except NoResultFound:
                return False, f"Pessoa física com ID {pessoa_fisica_id} não encontrada"
