from logzero import logger


class RetryError(Exception):
    def __init__(self, times):
        self.times = times

    def message(self):
        logger.error("RetryError:times=%s", self.times)

    def __str__(self):
        return "RetryError:times={}".format(self.times)
