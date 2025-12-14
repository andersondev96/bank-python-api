import pytest
from src.models.sqlite.settings.connection import db_connection_handler
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository

# db_connection_handler.connection_to_db()

@pytest.mark.skip(reason="interação com o banco")
def test_add_pessoa_fisica():
    renda_mensal= 9000
    idade=25
    nome_completo="João da Silva"
    celular="99999-999999"
    email="joao@example.com"
    categoria="Categoria A"
    saldo=10000

    repo = PessoaFisicaRepository(db_connection_handler)
    repo.create_pessoa_fisica(renda_mensal, idade, nome_completo, celular, email, categoria, saldo)

@pytest.mark.skip(reason="interação com o banco")
def test_get_pessoa_fisica():
    repo = PessoaFisicaRepository(db_connection_handler)
    pessoa_fisica = repo.get_pessoa_fisica(1)
    print(pessoa_fisica)
