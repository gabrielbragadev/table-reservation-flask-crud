from abc import ABC, abstractmethod
from app.domain.entities.user import User


class FlaskLoginHandlerInterface(ABC):

    @abstractmethod
    def login(self, user: User) -> None:
        pass

    @abstractmethod
    def logout(self) -> None:
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        pass

    @abstractmethod
    def find_current_user_id(self) -> int:
        pass

    @abstractmethod
    def find_current_user_is_authenticated(self) -> bool:
        pass
