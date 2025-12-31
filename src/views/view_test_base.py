from http import HTTPStatus
from src.views.http_types.http_request import HttpRequest


class ViewTestBase:
    """Classe base mixin para testes de Views."""

    def check_handle_acao_invalida(self, view):
        request = HttpRequest(body={"action": "acao_invalida"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.body["success"] is False
        assert "inválida" in response.body["message"]

    def check_handle_sem_acao(self, view):
        request = HttpRequest(body={})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Ação (action) é obrigatória" in response.body["message"]

    def check_sacar_sucesso(self, view, controller):
        controller.sacar.return_value = (True, "Saque realizado")
        request = HttpRequest(body={"action": "sacar", "valor": "500.0"}, param={"id": "1"})
        response = view.handle(request)
        controller.sacar.assert_called_once_with(1, 500.0)
        assert response.status_code == HTTPStatus.OK
        assert response.body["success"] is True

    def check_sacar_sem_id(self, view, controller):
        request = HttpRequest(body={"action": "sacar", "valor": "500.0"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Parâmetro 'id' é obrigatório" in response.body["message"]
        controller.sacar.assert_not_called()

    def check_sacar_sem_valor(self, view):
        request = HttpRequest(body={"action": "sacar"}, param={"id": "1"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'valor' é obrigatório" in response.body["message"]

    def check_sacar_valor_invalido(self, view):
        request = HttpRequest(body={"action": "sacar", "valor": "abc"}, param={"id": "1"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Campo 'valor' deve ser um número válido" in response.body["message"]

    def check_sacar_falha_saldo_insuficiente(self, view, controller):
        controller.sacar.return_value = (False, "Saldo insuficiente")
        request = HttpRequest(body={"action": "sacar", "valor": "10000.0"}, param={"id": "1"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.body["success"] is False

    def check_extrato_sucesso(self, view, controller):
        controller.extrato.return_value = (True, "Saldo: R$10000.00")
        request = HttpRequest(body={"action": "extrato"}, param={"id": "1"})
        response = view.handle(request)
        controller.extrato.assert_called_once_with(1)
        assert response.status_code == HTTPStatus.OK
        assert response.body["success"] is True

    def check_extrato_sem_id(self, view):
        request = HttpRequest(body={"action": "extrato"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert "Parâmetro 'id' é obrigatório" in response.body["message"]

    def check_extrato_nao_encontrado(self, view, controller):
        controller.extrato.return_value = (False, "Pessoa não encontrada")
        request = HttpRequest(body={"action": "extrato"}, param={"id": "999"})
        response = view.handle(request)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.body["success"] is False
