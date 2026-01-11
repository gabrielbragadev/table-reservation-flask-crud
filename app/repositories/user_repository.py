from typing import List
from app.models.user import User
from app.extensions import db


class UserRepository:

    def find_all(self) -> List[User]:
        user = User.query.all()
        return user

    def find_by_username(self, username: str) -> User:
        user = User.query.filter_by(username=username).first()
        return user

    def find_by_id(self, user_id: int) -> User:
        user = User.query.filter_by(id=user_id).first()
        return user

    def create(self, user: User) -> None:
        db.session.add(user)
        db.session.commit()
