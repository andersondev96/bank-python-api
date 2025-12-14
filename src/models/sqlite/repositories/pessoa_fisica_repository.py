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
