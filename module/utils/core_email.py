from module.utils.core_config import cf
import yagmail


def send(subject, contents):
    if cf.enable_mail:
        yag = yagmail.SMTP(user=cf.sender,
                           password=cf.authorization,
                           host=cf.host)
        yag.send(cf.receiver, subject, contents)
