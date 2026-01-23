from abc import ABC, abstractmethod


class CryptocodeHandlerInterface(ABC):

    @abstractmethod
    def encrypting(two_fa_secret: str):
        pass

    @abstractmethod
    def decrypting(encrypted_two_fa_secret: str):
        pass
