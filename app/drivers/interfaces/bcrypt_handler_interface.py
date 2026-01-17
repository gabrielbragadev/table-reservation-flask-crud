from abc import ABC, abstractmethod

from app.domain.entities.user import User


class BcryptHandlerInterface(ABC):

    @abstractmethod
    def generate_password_hash(self, password: bytes) -> bytes:
        pass

    @abstractmethod
    def verify_password(self, user: User, password: bytes) -> bool:
        pass
