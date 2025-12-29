# pylint: disable=redefined-outer-name
from http import HTTPStatus
from unittest.mock import MagicMock, Mock
import pytest
from src.views.pessoa_fisica_view import PessoaFisicaView
from src.controllers.pessoa_fisica_controller import PessoaFisicaController
from src.views.http_types.http_request import HttpRequest
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable

@pytest.fixture
def controller():
    return MagicMock(spec=PessoaFisicaController)

@pytest.fixture
def view(controller):
    return PessoaFisicaView(controller)

@pytest.fixture
def mock_pessoa_fisica():
    mock = Mock(spec=PessoaFisicaTable)
    mock.id = 1
    mock.renda_mensal = 5000.0
    mock.idade = 35
    mock.nome_completo = "João da Silva"
    mock.celular = "9999-8888"
    mock.email = "joao@example.com"
    mock.categoria = "Categoria A"
    mock.saldo = 10000.0
    return mock

class TestPessoaFisicaView:
    """Testes unitários completos para PessoaFisicaView."""

    # ----- TESTES DE AÇÃO INVÁLIDA -----

    def test_handle_acao_invalida(self, view):
        """Testa ação inválida retorna 400."""
        request = HttpRequest(body={"action": "acao_invalida"})
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.body == {
            "success": False,
            "message": "Ação 'acao_invalida' inválida"
        }

    def test_handle_sem_acao(self, view):
        """Testa request sem ação retorna 400."""
        request = HttpRequest(body={})
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Ação (action) é obrigatória" in response.body["message"]

    # ----- TESTES DE CRIAR -----

    def test_criar_sucesso(self, view, controller):
        """Testa criação com sucesso retorna 201."""
        dados_validos = {
            "action": "criar",
            "renda_mensal": 5000.0,
            "idade": 35,
            "nome_completo": "João da Silva",
            "celular": "9999-8888",
            "email": "joao@example.com",
            "categoria": "Categoria A",
            "saldo": 10000.0
        }
        request = HttpRequest(body=dados_validos)
        response = view.handle(request)

        controller.criar.assert_called_once_with(dados_validos)
        assert response.status_code == HTTPStatus.CREATED
        assert response.body["success"] is True
        assert "Criação de Pessoa Física realizado com sucesso" in response.body["message"]

    def test_criar_falta_campo_obrigatorio(self, view, controller):
        """Testa criação sem campo obrigatório retorna 400."""
        dados_invalidos = {
            "action": "criar",
            "idade": 35,
            # Falta renda_mensal
        }
        request = HttpRequest(body=dados_invalidos)
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'renda_mensal' é obrigatório" in response.body["message"]
        controller.criar.assert_not_called()

    def test_criar_erro_excecao(self, view, controller):
        """Testa criação com exceção do controller."""
        controller.criar.side_effect = Exception("Erro no banco")

        dados_validos = {
            "action": "criar",
            "renda_mensal": 5000.0,
            "idade": 35,
            "nome_completo": "João da Silva",
            "celular": "9999-8888",
            "email": "joao@example.com",
            "categoria": "Categoria A"
        }
        request = HttpRequest(body=dados_validos)
        response = view.handle(request)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Erro no banco" in response.body["message"]

    # ----- TESTES DE BUSCAR -----

    def test_buscar_sucesso(self, view, controller, mock_pessoa_fisica):
        """Testa busca com sucesso retorna 200 com dados."""
        controller.buscar.return_value = mock_pessoa_fisica

        request = HttpRequest(
            body={"action": "buscar"},
            param={"id": "1"}
        )
        response = view.handle(request)

        controller.buscar.assert_called_once_with(1)
        assert response.status_code == HTTPStatus.OK
        assert response.body["data"]["nome_completo"] == "João da Silva"
        assert response.body["data"]["saldo"] == 10000.0

    def test_buscar_sem_id(self, view, controller):
        """Testa busca sem parâmetro ID retorna 400."""
        request = HttpRequest(body={"action": "buscar"})
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Parâmetro 'id' é obrigatório" in response.body["message"]
        controller.buscar.assert_not_called()

    def test_buscar_nao_encontrado(self, view, controller):
        """Testa busca de ID não encontrado retorna 404."""
        controller.buscar.return_value = None

        request = HttpRequest(
            body={"action": "buscar"},
            param={"id": "999"}
        )
        response = view.handle(request)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert "Pessoa física com ID 999 não encontrada" in response.body["message"]

    # ----- TESTES DE SACAR -----

    def test_sacar_sucesso(self, view, controller):
        """Testa saque com sucesso."""
        controller.sacar.return_value = (True, "Saque de R$500.00 realizado")

        request = HttpRequest(
            body={"action": "sacar", "valor": "500.0"},
            param={"id": "1"}
        )
        response = view.handle(request)

        controller.sacar.assert_called_once_with(1, 500.0)
        assert response.status_code == HTTPStatus.OK
        assert response.body["success"] is True

    def test_sacar_sem_id(self, view, controller):
        """Testa saque sem ID."""
        request = HttpRequest(body={"action": "sacar", "valor": "500.0"})
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Parâmetro 'id' é obrigatório" in response.body["message"]
        controller.sacar.assert_not_called()

    def test_sacar_sem_valor(self, view):
        """Testa saque sem valor."""
        request = HttpRequest(
            body={"action": "sacar"},
            param={"id": "1"}
        )
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'valor' é obrigatório" in response.body["message"]

    def test_sacar_valor_invalido(self, view):
        """Testa saque com valor não numérico."""
        request = HttpRequest(
            body={"action": "sacar", "valor": "abc"},
            param={"id": "1"}
        )
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'valor' deve ser um número válido" in response.body["message"]

    def test_sacar_falha_saldo_insuficiente(self, view, controller):
        """Testa saque com falha (saldo insuficiente)."""
        controller.sacar.return_value = (False, "Saldo insuficiente")

        request = HttpRequest(
            body={"action": "sacar", "valor": "10000.0"},
            param={"id": "1"}
        )
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.body["success"] is False

    # ----- TESTES DE EXTRATO -----

    def test_extrato_sucesso(self, view, controller):
        """Testa extrato com sucesso."""
        controller.extrato.return_value = (True, "Saldo: R$10000.00")

        request = HttpRequest(
            body={"action": "extrato"},
            param={"id": "1"}
        )
        response = view.handle(request)

        controller.extrato.assert_called_once_with(1)
        assert response.status_code == HTTPStatus.OK
        assert response.body["success"] is True

    def test_extrato_sem_id(self, view):
        """Testa extrato sem ID."""
        request = HttpRequest(body={"action": "extrato"})
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Parâmetro 'id' é obrigatório" in response.body["message"]

    def test_extrato_nao_encontrado(self, view, controller):
        """Testa extrato de pessoa não encontrada."""
        controller.extrato.return_value = (False, "Pessoa não encontrada")

        request = HttpRequest(
            body={"action": "extrato"},
            param={"id": "999"}
        )
        response = view.handle(request)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.body["success"] is False
