from typing import Optional, Tuple
from src.models.sqlite.repositories.pessoa_juridica_repository import PessoaJuridicaRepository
from src.models.sqlite.entities.pessoa_juridica import PessoaJuridicaTable


class PessoaJuridicaController:
    def __init__(self, repository: PessoaJuridicaRepository) -> None:
        self.repository = repository

    def criar(self, dados: dict) -> None:
        self.repository.create_pessoa_juridica(
            faturamento=dados['faturamento'],
            idade=dados['idade'],
            nome_fantasia=dados['nome_fantasia'],
            celular=dados['celular'],
            email_corporativo=dados['email_corporativo'],
            categoria=dados['categoria'],
            saldo=dados.get('saldo', 0.0)
        )

    def buscar(self, pessoa_id: int) -> Optional[PessoaJuridicaTable]:
        return self.repository.read_pessoa_juridica(pessoa_id)

    def sacar(self, pessoa_id: int, valor: float) -> Tuple[bool, str]:
        return self.repository.sacar(pessoa_id, valor)

    def extrato(self, pessoa_id: int) -> Tuple[bool, str]:
        return self.repository.extrato(pessoa_id)
