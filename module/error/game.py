from logzero import logger


class GameNotFound(Exception):
    def __init__(self, name):
        self.name = name


class CanNotChooseDaiLiZhiHui(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("关卡%s未开启代理作战", self.name)


class NotInPreFight(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("未在选中关卡%s的界面", self.name)


class GameFail(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("在关卡%s中失败，请检查队伍配置", self.name)


class NotReason(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.warn("理智不足")


class ErrorPage(Exception):
    def __init__(self):
        pass

    def message(self):
        logger.warn("未期望的页面")
