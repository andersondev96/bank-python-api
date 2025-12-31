# pylint: disable=redefined-outer-name
from http import HTTPStatus
from unittest.mock import MagicMock, Mock
import pytest
from src.views.pessoa_juridica_view import PessoaJuridicaView
from src.controllers.pessoa_juridica_controller import PessoaJuridicaController
from src.views.http_types.http_request import HttpRequest
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable
from src.views.view_test_base import ViewTestBase

@pytest.fixture
def controller():
    return MagicMock(spec=PessoaJuridicaController)

@pytest.fixture
def view(controller):
    return PessoaJuridicaView(controller)

@pytest.fixture
def mock_pessoa_juridica():
    mock = Mock(spec=PessoaJuridicaTable)
    mock.id = 1
    mock.faturamento = 5000.0
    mock.idade = 35
    mock.nome_fantasia = "João da Silva"
    mock.celular = "9999-8888"
    mock.email_corporativo = "joao@example.com"
    mock.categoria = "Categoria A"
    mock.saldo = 10000.0
    return mock

class TestPessoaJuridicaView(ViewTestBase):
    """Testes unitários completos para PessoaJuridicaView."""

    # ----- TESTES DE AÇÃO INVÁLIDA -----

    def test_handle_acao_invalida(self, view):
        self.check_handle_acao_invalida(view)

    def test_handle_sem_acao(self, view):
        self.check_handle_sem_acao(view)

    # ----- TESTES DE CRIAR -----

    def test_criar_sucesso(self, view, controller):
        """Testa criação com sucesso retorna 201."""
        dados_validos = {
            "action": "criar",
            "faturamento": 5000.0,
            "idade": 35,
            "nome_fantasia": "João da Silva",
            "celular": "9999-8888",
            "email_corporativo": "joao@example.com",
            "categoria": "Categoria A",
            "saldo": 10000.0
        }
        request = HttpRequest(body=dados_validos)
        response = view.handle(request)

        controller.criar.assert_called_once_with(dados_validos)
        assert response.status_code == HTTPStatus.CREATED
        assert response.body["success"] is True
        assert "Criação de Pessoa Jurídica realizada com sucesso" in response.body["message"]

    def test_criar_falta_campo_obrigatorio(self, view, controller):
        """Testa criação sem campo obrigatório retorna 400."""
        dados_invalidos = {
            "action": "criar",
            "idade": 35,
            # Falta faturamento
        }
        request = HttpRequest(body=dados_invalidos)
        response = view.handle(request)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'faturamento' é obrigatório" in response.body["message"]
        controller.criar.assert_not_called()

    def test_criar_erro_excecao(self, view, controller):
        """Testa criação com exceção do controller."""
        controller.criar.side_effect = Exception("Erro no banco")

        dados_validos = {
            "action": "criar",
            "faturamento": 5000.0,
            "idade": 35,
            "nome_fantasia": "João da Silva",
            "celular": "9999-8888",
            "email_corporativo": "joao@example.com",
            "categoria": "Categoria A"
        }
        request = HttpRequest(body=dados_validos)
        response = view.handle(request)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert "Erro no banco" in response.body["message"]

    # ----- TESTES DE BUSCAR -----

    def test_buscar_sucesso(self, view, controller, mock_pessoa_juridica):
        """Testa busca com sucesso retorna 200 com dados."""
        controller.buscar.return_value = mock_pessoa_juridica

        request = HttpRequest(
            body={"action": "buscar"},
            param={"id": "1"}
        )
        response = view.handle(request)

        controller.buscar.assert_called_once_with(1)
        assert response.status_code == HTTPStatus.OK
        assert response.body["data"]["nome_fantasia"] == "João da Silva"
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
        assert "Pessoa jurídica com ID 999 não encontrada" in response.body["message"]

    # ----- TESTES DE SACAR -----

    def test_sacar_sucesso(self, view, controller):
        self.check_sacar_sucesso(view, controller)

    def test_sacar_sem_id(self, view, controller):
        self.check_sacar_sem_id(view, controller)

    def test_sacar_sem_valor(self, view):
        self.check_sacar_sem_valor(view)

    def test_sacar_valor_invalido(self, view):
        self.check_sacar_valor_invalido(view)

    def test_sacar_falha_saldo_insuficiente(self, view, controller):
        self.check_sacar_falha_saldo_insuficiente(view, controller)

    # ----- TESTES DE EXTRATO -----

    def test_extrato_sucesso(self, view, controller):
        self.check_extrato_sucesso(view, controller)

    def test_extrato_sem_id(self, view):
        self.check_extrato_sem_id(view)

    def test_extrato_nao_encontrado(self, view, controller):
        self.check_extrato_nao_encontrado(view, controller)
