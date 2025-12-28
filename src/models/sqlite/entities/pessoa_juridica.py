from sqlalchemy import Column, String, REAL, BIGINT
from src.models.sqlite.settings.base import Base

class PessoaJuridicaTable(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "pessoa_juridica"

    id = Column(BIGINT, primary_key=True)
    faturamento = Column(REAL, nullable=False)
    idade = Column(BIGINT, nullable=False)
    nome_fantasia = Column(String, nullable=False)
    celular = Column(String, nullable=False)
    email_corporativo = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    saldo = Column(REAL, nullable=False)

    def __repr__(self):
        return (
            f"PessoaJuridica("
            f"id={self.id}, "
            f"nome_fantasia={self.nome_fantasia}, "
            f"email={self.email_corporativo}, "
            f"categoria={self.categoria}, "
            f"saldo=R${self.saldo:.2f})"
        )
