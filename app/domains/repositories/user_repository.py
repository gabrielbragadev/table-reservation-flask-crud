from sqlalchemy.orm import Session
from typing import List
from app.domains.entities.user import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[User]:
        user = self.session.query(User).all()
        return user

    def find_by_username(self, username: str) -> User:
        user = self.session.query(User).filter_by(username=username).first()
        return user

    def find_by_id(self, user_id: int) -> User:
        user = self.session.query(User).filter_by(id=user_id).first()
        return user

    def create(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
