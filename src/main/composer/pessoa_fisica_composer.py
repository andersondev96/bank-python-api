from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository
from src.controllers.pessoa_fisica_controller import PessoaFisicaController
from src.views.pessoa_fisica_view import PessoaFisicaView

def pessoa_fisica_composer():
    db_connection_handler.connection_to_db()
    model = PessoaFisicaRepository(db_connection_handler)
    controller = PessoaFisicaController(model)
    view = PessoaFisicaView(controller)

    return view
