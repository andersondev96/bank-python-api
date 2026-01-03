from flask import Blueprint, jsonify, request
# pylint: disable=duplicate-code
from src.views.http_types.http_request import HttpRequest

from src.main.composer.pessoa_juridica_composer import pessoa_juridica_composer

pessoa_juridica_routes_bp = Blueprint("pessoa_juridica_routes", __name__)

@pessoa_juridica_routes_bp.route("/pessoa-juridica", methods=["POST"])
def create_pessoa_juridica():
    body = request.json or {}
    # Define a ação para o método handle processar corretamente
    body["action"] = "criar"
    http_request = HttpRequest(body=body)
    view = pessoa_juridica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code

@pessoa_juridica_routes_bp.route("/pessoa-juridica/<int:person_id>", methods=["GET"])
def get_pessoa_juridica(person_id):
    http_request = HttpRequest(
        body={ "action": "buscar" },
        param={ "id": person_id }
    )
    view = pessoa_juridica_composer()
    http_response = view.handle(http_request)

    return jsonify(http_response.body), http_response.status_code

@pessoa_juridica_routes_bp.route("/pessoa-juridica/<int:person_id>/sacar", methods=["POST"])
def sacar_pessoa_juridica(person_id):
    body = request.json or {}
    body["action"] = "sacar"
    http_request = HttpRequest(body=body, param={"id": person_id})
    view = pessoa_juridica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code

@pessoa_juridica_routes_bp.route("/pessoa-juridica/<int:person_id>/extrato", methods=["GET"])
def extrato_pessoa_juridica(person_id):
    http_request = HttpRequest(
        body={ "action": "extrato" },
        param={ "id": person_id }
    )
    view = pessoa_juridica_composer()
    http_response = view.handle(http_request)

    return jsonify(http_response.body), http_response.status_code
