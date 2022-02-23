from logzero import logger


class CharactersNotFound(Exception):
    def __init__(self):
        pass

    def message(self, index):
        logger.error("图片识别未发现文字,尝试重新识别%s次", index)
