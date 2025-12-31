from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.pessoa_fisica_composer import pessoa_fisica_composer

pessoa_fisica_routes_bp = Blueprint("pessoa_fisica_routes", __name__)

@pessoa_fisica_routes_bp.route("/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, World!"})


@pessoa_fisica_routes_bp.route("/pessoa-fisica", methods=["POST"])
def create_pessoa_fisica():
    body = request.json or {}
    # Define a ação para o método handle processar corretamente
    body["action"] = "criar"
    http_request = HttpRequest(body=body)
    view = pessoa_fisica_composer()

    http_response = view.handle(http_request)
    return jsonify(http_response.body), http_response.status_code
