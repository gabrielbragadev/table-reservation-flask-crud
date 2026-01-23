from typing import Dict
import pyotp
from app.domain.entities.user import User
from app.domain.rules.two_fa_rules import TwoFaRules
from app.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork
from app.domain.exceptions import NotFoundError


class RequestDeleteAccountService:
    def __init__(self, unit_of_work: UnitOfWork):
        self.__uow = unit_of_work

    def request_account_delete_otp(self, user: User) -> Dict:
        if not user:
            raise NotFoundError(message="Usuário é obrigatório")

        if not user.two_fa_secret:
            user.two_fa_secret = self.__generate_two_fa_secret()
            self.__uow.commit()

        totp = TwoFaRules.generate_totp(user.two_fa_secret)

        return {
            "message": "Confirme a exclusão com o código 2FA",
            "code_for_dev": totp.now(),  # ⚠️ REMOVER EM PROD
        }

    def __generate_two_fa_secret(self) -> str:
        return pyotp.random_base32()
