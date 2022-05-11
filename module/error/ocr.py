from logzero import logger


class CharactersNotFound(Exception):
    def __init__(self):
        pass

    def message(self, index):
        self.index = index
        logger.error("图片识别未发现文字,尝试重新识别%s次", self.index)

    def __str__(self):
        return "图片识别未发现文字,尝试重新识别{}次".format(self.index)


class OcrErr(Exception):
    def __init__(self, res):
        self.res = res
        pass

    def __str__(self):
        return "ocr出错,获取的内容:".format(self.res)
