from flask import Blueprint, jsonify, request
# pylint: disable=duplicate-code
from src.views.http_types.http_request import HttpRequest

from src.main.composer.pessoa_fisica_composer import pessoa_fisica_composer

from src.errors.error_handle import handle_errors

pessoa_fisica_routes_bp = Blueprint("pessoa_fisica_routes", __name__)

@pessoa_fisica_routes_bp.route("/pessoa-fisica", methods=["POST"])
def create_pessoa_fisica():
    try:
        body = request.json or {}
        # Define a ação para o método handle processar corretamente
        body["action"] = "criar"
        http_request = HttpRequest(body=body)
        view = pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@pessoa_fisica_routes_bp.route("/pessoa-fisica/<int:person_id>", methods=["GET"])
def get_pessoa_fisica(person_id):
    try:
        http_request = HttpRequest(
            body={ "action": "buscar" },
            param={ "id": person_id }
        )
        view = pessoa_fisica_composer()
        http_response = view.handle(http_request)

        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@pessoa_fisica_routes_bp.route("/pessoa-fisica/<int:person_id>/sacar", methods=["POST"])
def sacar_pessoa_fisica(person_id):
    try:
        body = request.json or {}
        body["action"] = "sacar"
        http_request = HttpRequest(body=body, param={"id": person_id})
        view = pessoa_fisica_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code

@pessoa_fisica_routes_bp.route("/pessoa-fisica/<int:person_id>/extrato", methods=["GET"])
def extrato_pessoa_fisica(person_id):
    try:
        http_request = HttpRequest(
            body={ "action": "extrato" },
            param={ "id": person_id }
        )
        view = pessoa_fisica_composer()
        http_response = view.handle(http_request)

        return jsonify(http_response.body), http_response.status_code
    except Exception as exception:
        http_response = handle_errors(exception)
        return jsonify(http_response.body), http_response.status_code
