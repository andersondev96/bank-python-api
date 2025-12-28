# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.controllers.pessoa_fisica_controller import PessoaFisicaController
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable


@pytest.fixture
def mock_repository():
    return MagicMock(spec=PessoaFisicaRepository)


@pytest.fixture
def controller(mock_repository):
    return PessoaFisicaController(mock_repository)


class TestPessoaFisicaController:

    def test_criar_sucesso(self, controller, mock_repository):
        dados = {
            "renda_mensal": 5000.0,
            "idade": 35,
            "nome_completo": "João da Silva",
            "celular": "9999-8888",
            "email": "joao@example.com",
            "categoria": "Categoria A",
            "saldo": 10000.0
        }

        controller.criar(dados)

        mock_repository.create_pessoa_fisica.assert_called_once_with(
            renda_mensal=5000.0,
            idade=35,
            nome_completo="João da Silva",
            celular="9999-8888",
            email="joao@example.com",
            categoria="Categoria A",
            saldo=10000.0
        )

    def test_buscar_sucesso(self, controller, mock_repository):
        mock_pf = MagicMock(spec=PessoaFisicaTable)
        mock_repository.get_pessoa_fisica.return_value = mock_pf

        resultado = controller.buscar(1)

        mock_repository.get_pessoa_fisica.assert_called_once_with(1)
        assert resultado == mock_pf

    def test_buscar_nao_encontrado(self, controller, mock_repository):
        mock_repository.get_pessoa_fisica.return_value = None

        resultado = controller.buscar(999)

        mock_repository.get_pessoa_fisica.assert_called_once_with(999)
        assert resultado is None

    def test_sacar_sucesso(self, controller, mock_repository):
        mock_repository.sacar.return_value = (True, "Saque realizado")

        resultado, mensagem = controller.sacar(1, 500.0)

        mock_repository.sacar.assert_called_once_with(1, 500.0)
        assert resultado is True
        assert "Saque realizado" in mensagem

    def test_sacar_falha(self, controller, mock_repository):
        mock_repository.sacar.return_value = (False, "Saldo insuficiente")

        resultado, mensagem = controller.sacar(1, 5000.0)

        mock_repository.sacar.assert_called_once_with(1, 5000.0)
        assert resultado is False
        assert "Saldo insuficiente" in mensagem

    def test_extrato_sucesso(self, controller, mock_repository):
        mock_repository.extrato.return_value = (True, "Saldo: R$1000")

        resultado, mensagem = controller.extrato(1)

        mock_repository.extrato.assert_called_once_with(1)
        assert resultado is True
        assert "Saldo: R$1000" in mensagem
