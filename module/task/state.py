import module.step.click_step
import module.step.judge_step
import module.step.gamepass_step
from module.utils.core_picture import *
from module.utils.core_email import *
from module.utils.core_clickLoader import ci
from module.utils.core_ocr import ocr_without_position

lizhi = {"time": "0", "lizhi": "0", "maxlizhi": "0"}
is_fight = "stop"
running_task_num = 0


# 获取当前理智
# 返回[当前理智,最大理智]
@func_set_timeout(timeout_time)
def get_lizhi():
    module.step.judge_step.ensureGameOpenAndInMain()
    time.sleep(1)
    module.step.gamepass_step.exec_by_clickLoader(ci["lizhi"])
    time.sleep(3)
    screen()
    time.sleep(3)
    region = read(screen_path)
    lizhi_before_fight = ui["lizhi_before_fight"]["area"]
    x1 = lizhi_before_fight[0]
    y1 = lizhi_before_fight[1]
    x2 = lizhi_before_fight[2]
    y2 = lizhi_before_fight[3]
    cropped = cut(region, x1, y1, x2, y2)
    write(screen_path, cropped)
    time.sleep(3)
    result = ocr_without_position(screen_path)
    logger.debug("获取理智内容是：" + str(result))
    dic = result[0]["words"].split("/")
    global lizhi
    lizhi["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lizhi["lizhi"] = dic[0]
    lizhi["maxlizhi"] = dic[1]
    module.step.judge_step.ensureGameOpenAndInMain()
