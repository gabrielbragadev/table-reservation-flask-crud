from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        user = self.session.query(User).all()
        return user

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
