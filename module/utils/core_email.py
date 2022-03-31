from module.utils.core_config import *
import yagmail

enable = configList["Config"]["Mail"]["enable"]
sender = configList["Config"]["Mail"]["sender"]
authorization = configList["Config"]["Mail"]["authorization"]
receiver = configList["Config"]["Mail"]["receiver"]
host = configList["Config"]["Mail"]["host"]


def send(subject, contents):
    if enable:
        yag = yagmail.SMTP(user=sender, password=authorization, host=host)
        yag.send(receiver, subject, contents)
