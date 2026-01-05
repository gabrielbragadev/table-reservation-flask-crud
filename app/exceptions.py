class ConflictError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class UnauthorizedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
