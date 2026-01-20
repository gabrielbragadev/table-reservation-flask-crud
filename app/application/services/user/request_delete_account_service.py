import pyotp
from app.domain.entities.user import User
from app.domain.rules.two_fa_rules import TwoFARules
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface
from app.infrastructure.persistence.sqlalchemy.unit_of_work import UnitOfWork


class RequestDeleteAccountService:
    def __init__(
        self, bcrypt_handler: BcryptHandlerInterface, unit_of_work: UnitOfWork
    ):
        self.__bcrypy_handler = bcrypt_handler
        self.__two_fa_secret = None
        self.__uow = unit_of_work

    def request(self, user: User):
        if not user.two_fa_secret:

            self.__generate_two_fa_secret()

            user.two_fa_secret = self.__two_fa_secret
            self.__uow.commit()

        totp = TwoFARules.generate_totp(user.two_fa_secret)

        return {
            "message": "Confirme a exclusão com o código 2FA",
            "code_for_dev": totp.now(),  # ⚠️ REMOVER EM PROD
        }

    def __generate_two_fa_secret(self):
        self.__two_fa_secret = self.__bcrypy_handler.generate_hash(
            str.encode(pyotp.random_base32())
        )
