import subprocess
import time
import random
import numpy
from .core_config import *
from .core_assetLoader import ui
import timeout_decorator
import cv2

os.system('chcp 65001')

ADB = configList["Config"]["Control"]["ADB"]
project_path = configList["Config"]["System"]["project_path"]
if ADB == "adb.exe":
    adb_path = "adb"
else:
    adb_path = project_path + ADB
connect_uri = configList["Config"]["Emulator"]["serial"]
package_name = configList["Config"]['Emulator']['package_name']
activity_name = configList["Config"]['Emulator']['activity_name']
enable_screen = configList["Config"]['Screen']['enable']
screen_debug = configList["Config"]['Screen']['debug']
port = " -s " + connect_uri + " "
screen_time = configList["Config"]['Screen']['time']


def connect():
    os.system(adb_path + ' connect {}'.format(connect_uri))
    logger.info('connect %s', connect_uri)


def disconnect():
    os.system(adb_path + ' disconnect {}'.format(connect_uri))
    logger.info('connect {}'.format(connect_uri))


def start():
    os.system(adb_path + port + ' shell am start -n {}/{}'.format(package_name,
                                                                  activity_name))
    logger.info("启动应用%s", package_name)


def stop():
    os.system(adb_path + port + ' shell am force-stop {}'.format(package_name))
    logger.info("关闭应用%s", package_name)


def isLive():
    with os.popen(adb_path + port + " shell ps", 'r') as f:
        text = f.read()
    if package_name in text:
        return True
    return False


def click(x, y):
    os.system(adb_path + port + " shell input tap {} {}".format(x, y))
    logger.info("click(%s,%s)", x, y)


def randomClick(name):
    if isinstance(name, str):
        obj = ui[name]
        x1 = obj["button"][0]
        y1 = obj["button"][1]
        x2 = obj["button"][2]
        y2 = obj["button"][3]
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        os.system(adb_path + port + " shell input tap {} {}".format(x, y))
        logger.info("randomClick(%s,%s)", x, y)
    elif isinstance(name, tuple):
        x1 = name[0]
        y1 = name[1]
        x2 = name[2]
        y2 = name[3]
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        os.system(adb_path + port + " shell input tap {} {}".format(x, y))
        logger.info("randomClick(%s,%s)", x, y)


# 从(x1, y1) 滑动至 (x2, y2) 时间为ctime
def scroll(x1, y1, x2, y2, ctime):
    os.system(adb_path + port + " shell input swipe {} {} {} {} {}".format(x1, y1, x2, y2, ctime))
    logger.info("scroll ({},{}) to ({},{}) cost {}".format(x1, y1, x2, y2, ctime))
    ctime = ctime / 1000
    if ctime <= 2:
        time.sleep(ctime + 5)
    elif 1 < ctime <= 3:
        time.sleep(ctime + 3)
    else:
        time.sleep(ctime + 1)


#
def scroll_by_tuple(name):
    x1 = name[0]
    y1 = name[1]
    x2 = name[2]
    y2 = name[3]
    ctime = name[4]
    os.system(adb_path + port + " shell input swipe {} {} {} {} {}".format(x1, y1, x2, y2, ctime))
    logger.info("scroll({},{}) to ({},{}) cost {}".format(x1, y1, x2, y2, ctime))
    ctime = ctime / 1000
    if ctime <= 2:
        time.sleep(ctime + 5)
    elif 1 < ctime <= 3:
        time.sleep(ctime + 3)
    else:
        time.sleep(ctime + 1)


# 截图至path
def screen(path="/cache/screen.png"):
    i = (project_path + path).rindex("/")
    dic_path = (project_path + path)[:i]
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)
    os.system(adb_path + port + ' shell screencap -p /sdcard/screen.png')
    os.system(adb_path + port + ' pull /sdcard/screen.png ' + project_path + path)
    time.sleep(screen_time)
    return project_path + path


def screen_memery():
    proc = subprocess.Popen(
        adb_path + port + ' shell screencap -p',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    # returncode 代表执行cmd命令报错
    # if proc.returncode > 0:
    #     raise Exception(proc.returncode, stderr)
    # opencv读取内存图片
    byteImage = stdout.replace(b'\r\r\n', b'\n')
    return cv2.imdecode(numpy.asarray(bytearray(byteImage), dtype=numpy.uint8), cv2.IMREAD_COLOR)



# 保存截图path 例如 /screenshots/test
def save(path):
    f_src = open(project_path + "/cache/screen.png", 'rb')
    store_path = project_path + path
    store_uri = store_path + "/" + str(time.time()) + ".png"
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    f_copy = open(store_uri, 'wb')
    if enable_screen:
        f_copy.write(f_src.read())
    f_src.close()
    f_copy.close()
    return store_uri


# 保存截图至/type1/type2/X.png
def save1(type1, type2):
    f_src = open(project_path + "/cache/screen.png", 'rb')
    store_path = project_path + "/screenshots/{}/{}".format(type1, type2)
    store_uri = store_path + "/" + str(time.time()) + ".png"
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    f_copy = open(store_uri, 'wb')
    if enable_screen:
        f_copy.write(f_src.read())
    f_src.close()
    f_copy.close()
    return store_uri


# 保存截图至/type/X.png
def save2(type):
    f_src = open(project_path + "/cache/screen.png", 'rb')
    store_path = project_path + "/screenshots/{}".format(type)
    store_uri = store_path + "/" + str(time.time()) + ".png"
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    f_copy = open(store_uri, 'wb')
    if enable_screen:
        f_copy.write(f_src.read())
    f_src.close()
    f_copy.close()
    return store_uri


def delScreen(uri):
    os.remove(uri)
    logger.debug("del screen  %s", uri)


connect()
