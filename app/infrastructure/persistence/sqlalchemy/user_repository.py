from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from typing import List
from app.domain.entities.user import User


class UserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        self.session.add(user)

    def find_by_id(self, user_id: int) -> User:
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def find_by_username(self, username: str) -> User:
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def find_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def find_all(self) -> List[User]:
        user = self.session.query(User).all()
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
