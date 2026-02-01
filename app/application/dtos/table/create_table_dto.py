from dataclasses import dataclass
from app.drivers.interfaces.bcrypt_handler_interface import BcryptHandlerInterface


@dataclass()
class CreateTableDTO:
    table_number: int
    people_capacity: int
