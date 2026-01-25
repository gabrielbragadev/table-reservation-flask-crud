class ConflictError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.name = "ConflictError"
        self.status_code = 409


class UnauthorizedError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.name = "UnauthorizedError"
        self.status_code = 401


class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.name = "NotFoundError"
        self.status_code = 404


class ForbiddenError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.name = "ForbiddenError"
        self.status_code = 403
