from src.controllers.base_controller import BaseController


class TestBaseController:

    def test_validar_dados_obrigatorios_sucesso(self):
        dados = {"nome": "João", "email": "joao@test.com"}
        is_valid, msg = BaseController.validar_dados_obrigatorios(dados, ["nome", "email"])
        assert is_valid is True
        assert msg == ""

    def test_validar_dados_obrigatorios_falha_nome(self):
        dados = {"email": "joao@test.com"}
        is_valid, msg = BaseController.validar_dados_obrigatorios(dados, ["nome", "email"])
        assert is_valid is False
        assert "Campo 'nome' é obrigatório" in msg

    def test_validar_dados_obrigatorios_falha_email_vazio(self):
        dados = {"nome": "João", "email": ""}
        is_valid, msg = BaseController.validar_dados_obrigatorios(dados, ["nome", "email"])
        assert is_valid is False
        assert "Campo 'email' é obrigatório" in msg

    def test_formatar_resposta_sucesso(self):
        resposta = BaseController.formatar_resposta_sucesso("Saque realizado com sucesso", "R$500")
        assert resposta == {
            "success": True,
            "message": "Saque realizado com sucesso",
            "details": "R$500"
        }

    def test_formatar_resposta_sucesso_sem_detalhes(self):
        resposta = BaseController.formatar_resposta_sucesso("Operação realizada")
        assert resposta == {
            "success": True,
            "message": "Operação realizada"
        }

    def test_formatar_resposta_erro(self):
        resposta = BaseController.formatar_resposta_erro("Saldo insuficiente")
        assert resposta == {
            "success": False,
            "message": "Saldo insuficiente"
        }
