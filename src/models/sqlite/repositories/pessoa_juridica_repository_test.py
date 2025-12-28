from unittest.mock import MagicMock
import pytest
from sqlalchemy.orm.exc import NoResultFound
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository
from src.models.sqlite.repositories.test_utils import MockConnection

def test_create_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)
    repo.create_pessoa_juridica(
        faturamento=1000,
        idade=5,
        nome_fantasia="Empresa A",
        celular="123456789",
        email_corporativo="joao@teste.com",
        categoria="Categoria A",
        saldo=5000
    )

    mock_connection.session.add.assert_called_once()
    mock_connection.session.commit.assert_called_once()

    added_company = mock_connection.session.add.call_args[0][0]
    assert added_company.faturamento == 1000
    assert added_company.idade == 5
    assert added_company.nome_fantasia == "Empresa A"
    assert added_company.celular == "123456789"
    assert added_company.email_corporativo == "joao@teste.com"
    assert added_company.categoria == "Categoria A"
    assert added_company.saldo == 5000

def test_create_pessoa_juridica_error():
    mock_connection = MockConnection()
    mock_connection.session.commit.side_effect = Exception("Erro de banco")
    repo = PessoaJuridicaRepository(mock_connection)

    with pytest.raises(Exception):
        repo.create_pessoa_juridica(
            faturamento=1000,
            idade=5,
            nome_fantasia="Empresa A",
            celular="123456789",
            email_corporativo="joao@teste.com",
            categoria="Categoria A",
            saldo=5000
        )

    mock_connection.session.rollback.assert_called_once()

def test_read_pessoa_juridica():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    expected_pj = PessoaJuridicaTable(id=1, nome_fantasia="Empresa A")
    mock_connection.session.query.return_value.filter.return_value.one.return_value = expected_pj

    response = repo.read_pessoa_juridica(1)

    mock_connection.session.query.assert_called_once()
    mock_connection.session.query.assert_called_once_with(PessoaJuridicaTable)

    mock_connection.session.query().filter.assert_called_once()
    # Compara a representação em string da expressão SQL para evitar erro de instância de objeto
    filter_call_arg = mock_connection.session.query().filter.call_args[0][0]
    expected_filter_expr = PessoaJuridicaTable.id == 1
    assert str(filter_call_arg) == str(expected_filter_expr)
    assert response == expected_pj

def test_read_pessoa_juridica_not_found():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    mock_connection.session.query.return_value.filter.return_value.one.side_effect = NoResultFound

    response = repo.read_pessoa_juridica(1)

    mock_connection.session.query.assert_called_once_with(PessoaJuridicaTable)
    assert response is None

def test_sacar_sucesso():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    mock_pj = MagicMock(spec=PessoaJuridicaTable)
    mock_pj.saldo = 2000.0
    mock_connection.session.query.return_value.filter.return_value.one.return_value = mock_pj

    resultado, mensagem = repo.sacar(1, 500.0)

    assert resultado is True
    assert "Saque de R$500.00 realizado com sucesso. Novo saldo: R$1500.00" in mensagem
    assert mock_pj.saldo == 1500.0
    mock_connection.session.commit.assert_called_once()

def test_extrato_sucesso():
    mock_connection = MockConnection()
    repo = PessoaJuridicaRepository(mock_connection)

    mock_pj = MagicMock(spec=PessoaJuridicaTable)
    mock_pj.saldo = 2500.0
    mock_connection.session.query.return_value.filter.return_value.one.return_value = mock_pj

    resultado, mensagem = repo.extrato(1)

    assert resultado is True
    assert "Extrato - Saldo atual: R$2500.00" in mensagem
