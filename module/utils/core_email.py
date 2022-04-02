from module.utils.core_config import cf
import yagmail


def send(subject, contents):
    if cf.get("enable_mail"):
        yag = yagmail.SMTP(user=cf.get("sender"),
                           password=cf.get("authorization"),
                           host=cf.get("host"))
        yag.send(cf.get("receiver"), subject, contents)
