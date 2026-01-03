from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository
from src.controllers.pessoa_fisica_controller import PessoaFisicaController
from src.controllers.pessoa_juridica_controller import PessoaJuridicaController


class ControllerFactory:

    @staticmethod
    def criar_pessoa_fisica_controller(db_conn) -> PessoaFisicaController:
        db_conn.connection_to_db()
        repository = PessoaFisicaRepository(db_conn)
        return PessoaFisicaController(repository)

    @staticmethod
    def criar_pessoa_juridica_controller(db_conn) -> PessoaJuridicaController:
        db_conn.connection_to_db()
        repository = PessoaJuridicaRepository(db_conn)
        return PessoaJuridicaController(repository)

    @classmethod
    def criar_todos(cls):
        return {
            "pessoa_fisica": cls.criar_pessoa_fisica_controller(db_connection_handler),
            "pessoa_juridica": cls.criar_pessoa_juridica_controller(db_connection_handler),
            "db_connection": db_connection_handler
        }
