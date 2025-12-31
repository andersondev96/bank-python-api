# pylint: disable=too-few-public-methods
from .http_types.http_response import HttpResponse
from .base_view import BaseView


class PessoaFisicaView(BaseView):
    def _criar(self, body: dict) -> HttpResponse:
        campos_obrigatorios = [
            "renda_mensal", "idade", "nome_completo",
            "celular", "email", "categoria"
        ]
        return self._helper_criar(
            body, campos_obrigatorios, "Criação de Pessoa Física realizada com sucesso"
        )

    def _buscar(self, params: dict) -> HttpResponse:
        def serializer(pessoa):
            return {
                "id": pessoa.id,
                "renda_mensal": float(pessoa.renda_mensal),
                "idade": int(pessoa.idade),
                "nome_completo": pessoa.nome_completo,
                "celular": pessoa.celular,
                "email": pessoa.email,
                "categoria": pessoa.categoria,
                "saldo": float(pessoa.saldo),
            }
        return self._helper_buscar(params, "Pessoa física", serializer)
