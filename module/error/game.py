from logzero import logger


class GameNotFound(Exception):
    def __init__(self, name):
        self.name = name


class CanNotChooseDaiLiZhiHui(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("关卡%s未开启代理作战", self.name)

    def __str__(self):
        return "关卡{}未开启代理作战".format(self.name)


class NotInPreFight(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("未在选中关卡%s的界面", self.name)

    def __str__(self):
        return "关未在选中关卡{}的界面".format(self.name)


class GameFail(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.error("在关卡%s中失败，请检查队伍配置", self.name)

    def __str__(self):
        return "关卡{}中失败，请检查队伍配置".format(self.name)


class NotReason(Exception):
    def __init__(self, name):
        self.name = name

    def message(self):
        logger.warn("理智不足")

    def __str__(self):
        return "理智不足"


class ErrorPage(Exception):
    def __init__(self):
        pass

    def message(self):
        logger.warn("未期望的页面")

    def __str__(self):
        return "未期望的页面"
