from module.utils.core_picture import *
from module.utils.core_ocr import ocr_without_position, number_ocr


def receive_daily_renwu():
    if compareSimilar("daily_renwu") >= 0.9:
        randomClick("daily_renwu")
        time.sleep(3)
        randomClick("renwu_receive")
        time.sleep(5)
        click(638, 645)


def receive_weekly_renwu():
    if compareSimilar("weekly_renwu") >= 0.9:
        randomClick("weekly_renwu")
        time.sleep(3)
        randomClick("renwu_receive")
        time.sleep(5)
        click(638, 645)


def friend_home():
    time.sleep(5)
    screen()
    region = read(screen_path)
    cropped = cut(region, 1187, 28, 1277, 52)
    write(screen_path, cropped)
    time.sleep(5)
    result = ocr_without_position(screen_path, number_ocr)
    pre = result[0]["words"]
    while True:
        randomClick("friend_home")
        time.sleep(8)
        screen()
        region = read(screen_path)
        cropped = cut(region, 1187, 28, 1277, 52)
        write(screen_path, cropped)
        result = ocr_without_position(screen_path)
        later = result[0]["words"]
        if pre == later:
            return
        pre = later
