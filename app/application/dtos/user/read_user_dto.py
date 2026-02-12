from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ReadUserDTO:
    user_id: int
    username: str
    email: int
    role: int

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }
