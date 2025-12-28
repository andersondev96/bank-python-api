# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock
import pytest
from src.controllers.pessoa_juridica_controller import PessoaJuridicaController
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository


@pytest.fixture
def mock_pj_repository():
    return MagicMock(spec=PessoaJuridicaRepository)


@pytest.fixture
def pj_controller(mock_pj_repository):
    return PessoaJuridicaController(mock_pj_repository)


class TestPessoaJuridicaController:

    def test_criar_sucesso(self, pj_controller, mock_pj_repository):
        dados = {
            "faturamento": 100000.0,
            "idade": 10,
            "nome_fantasia": "Empresa XYZ",
            "celular": "1111-2222",
            "email_corporativo": "contato@empresa.com",
            "categoria": "Categoria A",
            "saldo": 50000.0
        }

        pj_controller.criar(dados)

        mock_pj_repository.create_pessoa_juridica.assert_called_once_with(
            faturamento=100000.0,
            idade=10,
            nome_fantasia="Empresa XYZ",
            celular="1111-2222",
            email_corporativo="contato@empresa.com",
            categoria="Categoria A",
            saldo=50000.0
        )

    def test_buscar_sucesso(self, pj_controller, mock_pj_repository):
        mock_entity = MagicMock()
        mock_pj_repository.read_pessoa_juridica.return_value = mock_entity

        resultado = pj_controller.buscar(1)

        mock_pj_repository.read_pessoa_juridica.assert_called_once_with(1)
        assert resultado == mock_entity

    def test_sacar_sucesso(self, pj_controller, mock_pj_repository):
        mock_pj_repository.sacar.return_value = (True, "Saque PJ OK")

        resultado, _ = pj_controller.sacar(1, 2000.0)

        mock_pj_repository.sacar.assert_called_once_with(1, 2000.0)
        assert resultado is True

    def test_extrato_sucesso(self, pj_controller, mock_pj_repository):
        mock_pj_repository.extrato.return_value = (True, "Saldo PJ: R$50000")

        resultado, _ = pj_controller.extrato(1)

        mock_pj_repository.extrato.assert_called_once_with(1)
        assert resultado is True
