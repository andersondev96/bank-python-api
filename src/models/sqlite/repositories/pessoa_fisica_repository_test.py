from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository

class MockConnection:
    def __init__(self):
        self.session = MagicMock()

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

    added_person = mock_connection.session.add.call_args[0][0]
    assert added_person.renda_mensal == 9000
    assert added_person.idade == 25
    assert added_person.nome_completo == "João da Silva"
    assert added_person.celular == "99999-999999"
    assert added_person.email == "joao@example.com"
    assert added_person.categoria == "Categoria A"
    assert added_person.saldo == 10000

def test_insert_pessoa_fisica_error():
    mock_connection = MockConnection()
    mock_connection.session.commit.side_effect = Exception("Erro de banco")
    repo = PessoaFisicaRepository(mock_connection)

    with pytest.raises(Exception):
        repo.create_pessoa_fisica(
            renda_mensal=9000,
            idade=25,
            nome_completo="João da Silva",
            celular="99999-999999",
            email="joao@example.com",
            categoria="Categoria A",
            saldo=10000
        )

    mock_connection.session.rollback.assert_called_once()

def test_get_pessoa_fisica():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    expected_pf = PessoaFisicaTable(id=1, nome_completo="João da Silva")
    mock_connection.session.query.return_value.filter.return_value.one.return_value = expected_pf

    response = repo.get_pessoa_fisica(1)

    mock_connection.session.query.assert_called_once()
    mock_connection.session.query.assert_called_once_with(PessoaFisicaTable)

    mock_connection.session.query().filter.assert_called_once()
    # Compara a representação em string da expressão SQL para evitar erro de instância de objeto
    filter_call_arg = mock_connection.session.query().filter.call_args[0][0]
    expected_filter_expr = PessoaFisicaTable.id == 1
    assert str(filter_call_arg) == str(expected_filter_expr)
    assert response == expected_pf

def test_get_pessoa_fisica_not_found():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    mock_connection.session.query.return_value.filter.return_value.one.side_effect = NoResultFound

    response = repo.get_pessoa_fisica(1)

    mock_connection.session.query.assert_called_once_with(PessoaFisicaTable)
    assert response is None

def test_sacar_sucesso():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    mock_pf = MagicMock(spec=PessoaFisicaTable)
    mock_pf.saldo = 2000.0
    mock_connection.session.query.return_value.filter.return_value.one.return_value = mock_pf

    resultado, mensagem = repo.sacar(1, 500.0)

    assert resultado is True
    assert "Saque de R$500.00 realizado com sucesso. Novo saldo: R$1500.00" in mensagem
    assert mock_pf.saldo == 1500.0
    mock_connection.session.commit.assert_called_once()

def test_extrato_sucesso():
    mock_connection = MockConnection()
    repo = PessoaFisicaRepository(mock_connection)

    mock_pf = MagicMock(spec=PessoaFisicaTable)
    mock_pf.saldo = 2500.0
    mock_connection.session.query.return_value.filter.return_value.one.return_value = mock_pf

    resultado, mensagem = repo.extrato(1)

    assert resultado is True
    assert "Extrato - Saldo atual: R$2500.00" in mensagem
