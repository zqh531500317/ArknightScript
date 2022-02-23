import time


import module.task.daily
import module.task.huodong
import module.task.jijian
import module.utils.core_control
import module.utils.core_template
from module.utils.core_init import init
from module.utils.core_control import screen
from module.utils.core_ocr import *
from module.utils.core_picture import *
from module.utils.core_template import *
from PIL import Image
import module.step.recruit_step
from cnstd import CnStd
import cv2
import module.step.jijian_step


def test_daily():
    module.task.daily.friend()
    module.task.daily.receive_renwu()
    module.task.daily.receive_xinyong()
    module.task.daily.recruit_daily()
    module.task.daily.buy_xinyong_shop()


def test_fight():
    module.task.huodong.huodong("IW-6", 99, False, 0, False, 0)


def test_jijian():
    module.task.jijian.jijian_receive()
    module.task.jijian.use_electricity()


if __name__ == '__main__':
    init()
    screen()
    from cnstd import CnStd
    from cnocr import CnOcr

    std = CnStd()
    cn_ocr = CnOcr(cand_alphabet="1234567890-")

    box_infos = std.detect(screen_path)

    for box_info in box_infos['detected_texts']:
        cropped_img = box_info['cropped_img']
        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        print('ocr result: %s' % str(ocr_res))

    # region = read(screen_path)
    # cropped = cut(region, 766, 25, 863, 48)  # 基建无人机
    # cropped = cut(region, 585, 193, 687, 225)#判断剿灭是否打完
    # cropped = cut(region, 1187, 28, 1277, 52)  # 拜访好友是否变化
    # cropped =cut(region, 1116, 20, 1245, 57)  # 获取理智
    # write(screen_path,cropped)
    # ocr_without_position(screen_path)
