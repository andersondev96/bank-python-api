from abc import ABC
from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.orm.exc import NoResultFound

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    # pylint: disable=too-few-public-methods
    def __init__(self, db_connection, model: Type[T]) -> None:
        self.db_connection = db_connection
        self.model = model

    def _get_by_id(self, entity_id: int) -> Optional[T]:
        with self.db_connection as database:
            try:
                entity = (
                    database.session.query(self.model)
                    .filter(self.model.id == entity_id)
                    .one()
                )
                return entity
            except NoResultFound:
                return None

    def _validate_withdrawal_amount(self, valor: float) -> tuple[bool, str]:
        if valor <= 0:
            return False, "O valor do saque deve ser maior que zero"
        return True, ""

    def _check_balance(self, saldo: float, valor: float) -> tuple[bool, str]:
        if valor > saldo:
            return False, f"Saldo insuficiente. Saldo atual: R${saldo:.2f}"
        return True, ""

    def _check_withdrawal_limit(
        self,
        valor: float,
        limite: float,
        tipo_pessoa: str
    ) -> tuple[bool, str]:
        if valor > limite:
            return False, f"Saque excede o limite diário para {tipo_pessoa}: R${limite:.2f}"
        return True, ""

    def _perform_withdrawal(
        self,
        entity: T,
        valor: float,
        database
    ) -> None:
        entity.saldo -= valor
        database.session.commit()

    def _create_entity(self, entity_data: T) -> None:
        with self.db_connection as database:
            try:
                database.session.add(entity_data)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def _sacar_generic(
        self,
        entity_id: int,
        valor: float,
        limite_diario: float,
        tipo_pessoa: str,
        nome_entidade: str
    ) -> tuple[bool, str]:
        is_valid, error_msg = self._validate_withdrawal_amount(valor)
        if not is_valid:
            return False, error_msg

        with self.db_connection as database:
            try:
                try:
                    entity = (
                        database.session.query(self.model)
                        .filter(self.model.id == entity_id)
                        .one()
                    )
                except NoResultFound:
                    return False, f"{nome_entidade} com ID {entity_id} não encontrada"

                is_valid, error_msg = self._check_balance(entity.saldo, valor)
                if not is_valid:
                    return False, error_msg

                is_valid, error_msg = self._check_withdrawal_limit(
                    valor,
                    limite_diario,
                    tipo_pessoa
                )
                if not is_valid:
                    return False, error_msg

                self._perform_withdrawal(entity, valor, database)

                return True, (
                    f"Saque de R${valor:.2f} realizado com sucesso. "
                    f"Novo saldo: R${entity.saldo:.2f}"
                )
            except Exception as exception:
                database.session.rollback()
                raise exception
