from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository

class MockConnection:
    def __init__(self):
        self.session = UnifiedAlchemyMagicMock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def test_insert_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    repo.create_pessoa_fisica(
        renda_mensal=9000,
        idade=25,
        nome_completo="João da Silva",
        celular="99999-999999",
        email="joao@example.com",
        categoria="Categoria A",
        saldo=10000
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

def test_get_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    repo.get_pessoa_fisica(1)

    mock_connection.session.query.assert_called_once()
    mock_connection.session.query.assert_called_once_with(PessoaFisicaTable)
    mock_connection.session.query().filter.assert_called_once_with(PessoaFisicaTable.id == 1)
