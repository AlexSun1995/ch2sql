class UnknownDataSourceTypeException(BaseException):
    def __init__(self, reason=''):
        self.reason = reason

    def __str__(self):
        return self.reason


class IllegalQueryException(BaseException):
    def __init__(self, reason=''):
        self.reason = reason

    def __str__(self):
        return self.reason
