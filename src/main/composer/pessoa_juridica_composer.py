from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository
from src.controllers.pessoa_juridica_controller import PessoaJuridicaController
from src.views.pessoa_juridica_view import PessoaJuridicaView

def pessoa_juridica_composer():
    db_connection_handler.connection_to_db()
    model = PessoaJuridicaRepository(db_connection_handler)
    controller = PessoaJuridicaController(model)
    view = PessoaJuridicaView(controller)

    return view
