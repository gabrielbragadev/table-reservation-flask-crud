from dataclasses import dataclass


@dataclass()
class UserLoginDTO:
    username: str
    password: str

    def to_bytes(self) -> None:
        self.password = str.encode(self.password)
