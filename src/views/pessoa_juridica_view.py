# pylint: disable=too-few-public-methods
from .http_types.http_response import HttpResponse
from .base_view import BaseView


class PessoaJuridicaView(BaseView):
    def _criar(self, body: dict) -> HttpResponse:
        campos_obrigatorios = [
            "faturamento", "idade", "nome_fantasia",
            "celular", "email_corporativo", "categoria"
        ]
        return self._helper_criar(
            body, campos_obrigatorios, "Criação de Pessoa Jurídica realizada com sucesso"
        )

    def _buscar(self, params: dict) -> HttpResponse:
        def serializer(pessoa):
            return {
                "id": pessoa.id,
                "faturamento": float(pessoa.faturamento),
                "idade": int(pessoa.idade),
                "nome_fantasia": pessoa.nome_fantasia,
                "celular": pessoa.celular,
                "email_corporativo": pessoa.email_corporativo,
                "categoria": pessoa.categoria,
                "saldo": float(pessoa.saldo),
            }
        return self._helper_buscar(params, "Pessoa jurídica", serializer)
