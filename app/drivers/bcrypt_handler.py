import bcrypt
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface
from app.domain.entities.user import User


class BcryptHandler(BcryptHandlerInterface):

    def __init__(self) -> None:
        self.__bcrypt = bcrypt

    def generate_hash(self, password: bytes) -> bytes:
        return self.__bcrypt.hashpw(password, self.__bcrypt.gensalt())

    def verify_hash(self, user: User, password: bytes) -> bool:
        verify_hash = self.__bcrypt.checkpw(password, user.password)

        return verify_hash
