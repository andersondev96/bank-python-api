# pylint: disable=redefined-outer-name, too-few-public-methods
from http import HTTPStatus
from src.controllers.pessoa_juridica_controller import PessoaJuridicaController
from src.controllers.base_controller import BaseController
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface

class PessoaJuridicaView(ViewInterface):
    def __init__(self, controller: PessoaJuridicaController) -> None:
        self.__controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body or {}
        params = http_request.param or {}

        action = body.get("action")
        if not action:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body={
                    "success": False,
                    "message": "Ação (action) é obrigatória"
                }
            )

        if action == "criar":
            return self._criar(body)

        if action == "buscar":
            return self._buscar(params)

        if action == "sacar":
            return self._sacar(body, params)

        if action == "extrato":
            return self._extrato(params)

        return HttpResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            body={
                "success": False,
                "message": f"Ação '{action}' inválida"
            }
        )

    def _criar(self, body: dict) -> HttpResponse:
        campos_obrigatorios = [
            "faturamento", "idade", "nome_fantasia",
            "celular", "email_corporativo", "categoria"
        ]

        is_valid, msg = BaseController.validar_dados_obrigatorios(body, campos_obrigatorios)
        if not is_valid:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro(msg),
            )

        try:
            self.__controller.criar(body)
            resposta = BaseController.formatar_resposta_sucesso("Criação de Pessoa Jurídica")
            return HttpResponse(status_code=HTTPStatus.CREATED, body=resposta)
        except Exception as exc:
            return HttpResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=BaseController.formatar_resposta_erro(str(exc)),
            )

    def _buscar(self, params: dict) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro("Parâmetro 'id' é obrigatório"),
            )

        pessoa = self.__controller.buscar(int(pessoa_id))
        if pessoa is None:
            return HttpResponse(
                status_code=HTTPStatus.NOT_FOUND,
                body=BaseController.formatar_resposta_erro(
                    f"Pessoa jurídica com ID {pessoa_id} não encontrada"
                ),
            )

        return HttpResponse(
            status_code=HTTPStatus.OK,
            body={
                "success": True,
                "data": {
                    "id": pessoa.id,
                    "faturamento": float(pessoa.faturamento),
                    "idade": int(pessoa.idade),
                    "nome_fantasia": pessoa.nome_fantasia,
                    "celular": pessoa.celular,
                    "email_corporativo": pessoa.email_corporativo,
                    "categoria": pessoa.categoria,
                    "saldo": float(pessoa.saldo),
                },
            }
        )

    def _sacar(self, body: dict, params: dict) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro("Parâmetro 'id' é obrigatório"),
            )

        if "valor" not in body:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro("Campo 'valor' é obrigatório"),
            )

        try:
            valor = float(body["valor"])
        except (TypeError, ValueError):
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro(
                    "Campo 'valor' deve ser um número válido"
                ),
            )

        sucesso, mensagem = self.__controller.sacar(int(pessoa_id), valor)
        status = HTTPStatus.OK if sucesso else HTTPStatus.BAD_REQUEST
        body_resp = (
            BaseController.formatar_resposta_sucesso("Saque", mensagem)
            if sucesso
            else BaseController.formatar_resposta_erro(mensagem)
        )
        return HttpResponse(status_code=status, body=body_resp)

    def _extrato(self, params: dict) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            return HttpResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                body=BaseController.formatar_resposta_erro("Parâmetro 'id' é obrigatório"),
            )

        sucesso, mensagem = self.__controller.extrato(int(pessoa_id))
        status = HTTPStatus.OK if sucesso else HTTPStatus.NOT_FOUND
        body_resp = (
            BaseController.formatar_resposta_sucesso("Extrato", mensagem)
            if sucesso
            else BaseController.formatar_resposta_erro(mensagem)
        )
        return HttpResponse(status_code=status, body=body_resp)
