from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ReadUserDTO:
    username: str
    email: int
    role: int

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }
