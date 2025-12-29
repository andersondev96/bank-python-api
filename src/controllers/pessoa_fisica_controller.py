from typing import Optional, Tuple
from src.models.sqlite.repositories.pessoa_fisica_repository import PessoaFisicaRepository
from src.models.sqlite.entities.pessoa_fisica import PessoaFisicaTable
from .interfaces.pessoa_fisica_controller import PessoaFisicaControllerInterface


class PessoaFisicaController(PessoaFisicaControllerInterface):
    def __init__(self, repository: PessoaFisicaRepository) -> None:
        self.repository = repository

    def criar(self, dados: dict) -> None:
        self.repository.create_pessoa_fisica(
            renda_mensal=dados['renda_mensal'],
            idade=dados['idade'],
            nome_completo=dados['nome_completo'],
            celular=dados['celular'],
            email=dados['email'],
            categoria=dados['categoria'],
            saldo=dados.get('saldo', 0.0)
        )

    def buscar(self, pessoa_id: int) -> Optional[PessoaFisicaTable]:
        return self.repository.get_pessoa_fisica(pessoa_id)

    def sacar(self, pessoa_id: int, valor: float) -> Tuple[bool, str]:
        return self.repository.sacar(pessoa_id, valor)

    def extrato(self, pessoa_id: int) -> Tuple[bool, str]:
        return self.repository.extrato(pessoa_id)
