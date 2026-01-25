from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class UpdateUserDTO:
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            k: v
            for k, v in {
                "username": self.username,
                "email": self.email,
                "role": self.role,
            }.items()
            if v is not None
        }
