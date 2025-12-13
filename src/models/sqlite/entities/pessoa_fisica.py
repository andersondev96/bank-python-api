from sqlalchemy import Column, String, REAL, BIGINT
from src.models.sqlite.settings.base import Base

class PessoaFisica(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "pessoa_fisica"

    id = Column(BIGINT, primary_key=True)
    renda_mensal = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_completo = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    saldo = Column(REAL, nullable=False)

    def __repr__(self):
        return (
            f"PessoaFisica: [name={self.nome_completo}, email={self.email}, "
            f"celular={self.celular}, categoria={self.categoria}, saldo={self.saldo}]"
        )
