from dataclasses import dataclass
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface


@dataclass()
class CreateUserDTO:
    username: str
    password: str
    email: str
    role: str

    def encode_and_hashed_password(
        self, bcrypt_handler: BcryptHandlerInterface
    ) -> None:
        self.password = str.encode(self.password)
        self.password = bcrypt_handler.generate_hash(self.password)

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role,
        }
