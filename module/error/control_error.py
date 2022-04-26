from logzero import logger


class AcceptDataError(Exception):
    def __init__(self, data):
        self.data = data
