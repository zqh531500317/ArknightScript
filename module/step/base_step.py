from module.base import *
from module.entity.ocr_entity import OcrEntity
from module.entity.template_entity import TemplateEntity
from module.error.retryError import RetryError


class BaseStep:
    # ck 点击   template 期望匹配的 模板匹配路径 或 ocr结果
    # ck 1、str 2、(x1,y1,x2,y2)
    # template  1、str :template 2、OcrrEntity 3、function or method
    @staticmethod
    def dowait(ck, template,
               max_retry_times=3,
               retry_time=20.0, description=None, sleep_time=None):
        def log_msg(msg):
            if msg is not None:
                logger.info(msg)

        if sleep_time is None:
            sleep_time = base.sleep_time
        retry_times = 0
        start_time = time.time()
        base.randomClick(ck)
        while True:
            if isinstance(template, str):
                if base.is_template_match(template):
                    log_msg(description)
                    return True
            elif isinstance(template, TemplateEntity):
                if template.is_match():
                    log_msg(description)
                    return True
            elif isinstance(template, OcrEntity):
                if base.ocr(template).is_except():
                    log_msg(description)
                    return True
            elif isinstance(template, types.FunctionType) or isinstance(template, types.MethodType):
                bs = template()
                if bs:
                    log_msg(description)
                    return True
            time.sleep(sleep_time)
            now = time.time()
            if (now - start_time) > retry_time:
                if retry_times == max_retry_times:
                    logger.error("RetryError:times=%s", max_retry_times)
                    raise RetryError(retry_times)
                logger.warning("running time >%s,retry the %s times,description=%s", retry_time, retry_times,
                               description)
                base.randomClick(ck)
                retry_times += 1
                start_time = now

    @staticmethod
    def dowaitlist(list: List[
        Tuple[Union[str, tuple], Union[str, OcrEntity, types.FunctionType, types.MethodType], Union[str, None]]],
                   delay_time=0.1, max_retry_times=3, retry_time=20.0):
        for ck, templete, description in list:
            BaseStep.dowait(ck, templete, max_retry_times=max_retry_times, retry_time=retry_time,
                            description=description)
            time.sleep(delay_time)
