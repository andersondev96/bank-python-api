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
