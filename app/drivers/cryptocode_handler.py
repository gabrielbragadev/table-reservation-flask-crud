from typing import Literal
import cryptocode
import os
from dotenv import load_dotenv

from app.drivers.interfaces.cryptocode_handler_interface import (
    CryptocodeHandlerInterface,
)


class CryptocodeHandler(CryptocodeHandlerInterface):

    def __init__(self):
        load_dotenv()
        self.__crypto_password = os.getenv("CRYPTO_PASSWORD")

    def encrypting(self, two_fa_secret: str) -> str:

        encrypted_two_fa_secret = cryptocode.encrypt(
            two_fa_secret, self.__crypto_password
        )
        return encrypted_two_fa_secret

    def decrypting(self, encrypted_two_fa_secret: str) -> str | Literal[False]:
        decrypted_two_fa_secret = cryptocode.decrypt(
            encrypted_two_fa_secret, self.__crypto_password
        )
        return decrypted_two_fa_secret
