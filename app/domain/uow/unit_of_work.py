from abc import ABC


class UnitOfWork(ABC):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
