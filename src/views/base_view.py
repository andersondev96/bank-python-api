# pylint: disable=too-few-public-methods
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Callable, Any, List

from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from src.controllers.base_controller import BaseController
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from .interfaces.view_interface import ViewInterface


class BaseView(ViewInterface, ABC):
    def __init__(self, controller) -> None:
        self._controller = controller

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        try:
            body = http_request.body or {}
            params = http_request.param or {}

            action = body.get("action")
            if not action:
                raise HttpBadRequestError("Ação (action) é obrigatória")

            if action == "criar":
                return self._criar(body)

            if action == "buscar":
                return self._buscar(params)

            if action == "sacar":
                return self._sacar(body, params)

            if action == "extrato":
                return self._extrato(params)

            raise HttpBadRequestError(f"Ação '{action}' inválida")

        except (HttpBadRequestError, HttpNotFoundError, HttpUnprocessableEntityError) as exc:
            return HttpResponse(
                status_code=exc.status_code,
                body=BaseController.formatar_resposta_erro(exc)
            )
        except Exception as exc:
            return HttpResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                body=BaseController.formatar_resposta_erro(exc)
            )

    @abstractmethod
    def _criar(self, body: dict) -> HttpResponse:
        pass

    @abstractmethod
    def _buscar(self, params: dict) -> HttpResponse:
        pass

    def _sacar(self, body: dict, params: dict) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            raise HttpBadRequestError("Parâmetro 'id' é obrigatório")

        if "valor" not in body:
            raise HttpBadRequestError("Campo 'valor' é obrigatório")

        try:
            valor = float(body["valor"])
        except (TypeError, ValueError) as exc:
            raise HttpBadRequestError("Campo 'valor' deve ser um número válido") from exc

        sucesso, mensagem = self._controller.sacar(int(pessoa_id), valor)
        if not sucesso:
            raise HttpBadRequestError(mensagem)

        return HttpResponse(
            status_code=HTTPStatus.OK,
            body=BaseController.formatar_resposta_sucesso("Saque realizado com sucesso", mensagem)
        )

    def _extrato(self, params: dict) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            raise HttpBadRequestError("Parâmetro 'id' é obrigatório")

        _, mensagem = self._controller.extrato(int(pessoa_id))
        # Se falhar, o controller/repository lança exceção que é capturada no handle
        return HttpResponse(
            status_code=HTTPStatus.OK,
            body=BaseController.formatar_resposta_sucesso("Extrato gerado com sucesso", mensagem)
        )

    def _helper_criar(self, body: dict, campos: List[str], msg_sucesso: str) -> HttpResponse:
        is_valid, msg = BaseController.validar_dados_obrigatorios(body, campos)
        if not is_valid:
            raise HttpBadRequestError(msg)

        self._controller.criar(body)
        resposta = BaseController.formatar_resposta_sucesso(msg_sucesso)
        return HttpResponse(status_code=HTTPStatus.CREATED, body=resposta)

    def _helper_buscar(
        self, params: dict, entity_name: str, serializer: Callable[[Any], dict]
    ) -> HttpResponse:
        pessoa_id = params.get("id")
        if pessoa_id is None:
            raise HttpBadRequestError("Parâmetro 'id' é obrigatório")

        pessoa = self._controller.buscar(int(pessoa_id))
        if pessoa is None:
            raise HttpNotFoundError(f"{entity_name} com ID {pessoa_id} não encontrada")

        return HttpResponse(
            status_code=HTTPStatus.OK,
            body={
                "success": True,
                "data": serializer(pessoa),
            },
        )
