from dataclasses import dataclass
from typing import List, Dict

from app.application.dtos.user.read_user_dto import ReadUserDTO


@dataclass(frozen=True)
class ReadUsersDTO:
    users: List[ReadUserDTO]

    def to_list_of_dicts(self) -> List[Dict]:
        return [r.to_dict() for r in self.users]
