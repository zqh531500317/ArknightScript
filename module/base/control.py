import os
import random
import socket
import time
import typing
import adbutils
from retrying import retry
import numpy
import cv2
from module.base.log import Log
from module.base.store import Store
from module.utils.core_assetLoader import ui
from module.utils.core_utils import recv_all, random_port
from logzero import logger
from typing import Union
from module.error.control_error import AcceptDataError


class BaseAdb(Log, Store):
    def __init__(self):
        super().__init__()
        logger.debug("初始化BaseAdb")
        self.adb_client = adbutils.AdbClient('127.0.0.1', 5037)
        self.connect()
        self.adb = adbutils.AdbDevice(self.adb_client, self.serial)
        logger.info("class BaseAdb __init__")
        self.recent_img = None

    def connect(self):
        try:
            msg = self.adb_client.connect(self.serial, timeout=5)
            logger.info(msg)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    def disconnect(self):
        msg = self.adb_client.disconnect(self.serial)
        logger.info(msg)

    def start(self):
        self.stop()
        self.adb.app_start(self.package_name, self.activity_name)
        logger.info("启动应用%s", self.package_name)

    def stop(self):
        self.adb.app_stop(self.package_name)
        logger.info("关闭应用%s", self.package_name)

    def isLive(self):
        text = self.adb.current_app()["package"]
        if self.package_name == text:
            return True
        return False

    # return (package,activity)
    def getPackageNameAndActivityName(self) -> typing.Tuple[str, str]:
        text = self.adb.current_app()
        return text["package"], text["activity"]


class Adb(BaseAdb):
    __screenshot_method = [0, 1, 2]
    __screenshot_method_fixed = [0, 1, 2]

    def __init__(self):
        super().__init__()
        self.server = None
        logger.info("class Adb __init__")

    def randomClick(self, name: Union[str, tuple]):
        if isinstance(name, str):
            if name == "":
                return
            obj = ui[name]
            x1 = obj["button"][0]
            y1 = obj["button"][1]
            x2 = obj["button"][2]
            y2 = obj["button"][3]
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
            self.adb.click(x, y)
            logger.info("randomClick(%s,%s)", x, y)
        elif isinstance(name, tuple):
            if len(name) == 2:
                x = name[0]
                y = name[1]
                self.click(x, y)
            elif len(name) == 4:
                x1 = name[0]
                y1 = name[1]
                x2 = name[2]
                y2 = name[3]
                x = random.randint(x1, x2)
                y = random.randint(y1, y2)
                self.click(x, y)
                logger.info("randomClick(%s,%s)", x, y)

    def click(self, x, y):
        self.adb.click(x, y)
        logger.info("click(%s,%s)", x, y)

    def screen(self, path="/cache/screen.png", memery=True):
        if memery:
            img = self.__screen_memery()
            self.store_add_img(img)
            return img
        else:
            return self.__screen_disk(path)

    def scroll(self, x1, y1, x2, y2, ctime):
        cmd = ["input", "swipe"]
        cmd += [x1, y1, x2, y2, ctime]
        cmd = list(map(str, cmd))
        self.adb.shell(cmd)
        logger.info("scroll ({},{}) to ({},{}) cost {}".format(x1, y1, x2, y2, ctime))
        ctime = ctime / 1000
        if ctime <= 2:
            time.sleep(ctime + 5)
        elif 1 < ctime <= 3:
            time.sleep(ctime + 3)
        else:
            time.sleep(ctime + 1)

    def scroll_by_tuple(self, name):
        x1 = name[0]
        y1 = name[1]
        x2 = name[2]
        y2 = name[3]
        ctime = name[4]
        self.scroll(x1, y1, x2, y2, ctime)

    # 保存截图path 例如 /screenshots/test
    def save(self, path: str, img_path=None) -> str:
        if img_path is None:
            f_src = open(self.project_path + "/cache/screen.png", 'rb')
            img = f_src.read()
            f_src.close()
        else:
            img = img_path
        store_path = self.project_path + path
        store_uri = store_path + "/" + str(int(time.time())) + ".png"
        if not os.path.exists(store_path):
            os.makedirs(store_path)
        if img_path is None:
            f_copy = open(store_uri, 'wb')
            if self.get("enable_screen"):
                f_copy.write(img)
            f_copy.close()
        else:
            cv2.imwrite(store_uri, img)
        return store_uri

    # 保存截图至/type1/type2/X.png
    def save1(self, type1: str, type2: str, img_path=None) -> str:
        path = "/screenshots/{}/{}".format(type1, type2)

        return self.save(path, img_path=img_path)

    # 保存截图至/type/X.png
    def save2(self, type: str, img_path=None) -> str:
        path = "/screenshots/{}".format(type)
        return self.save(path, img_path=img_path)

    def __reverse_server(self):
        if self.server is None:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Create new reverse
            _server_port = self.__adb_reverse(f'tcp:7904')

            server.bind(('127.0.0.1', _server_port))
            server.listen(5)
            self.server = server
        else:
            server = self.server
        return server

    def __adb_reverse(self, remote):
        port = 0
        for reverse in self.adb.reverse_list():
            if reverse.remote == remote and reverse.local.startswith('tcp:'):
                if not port:
                    logger.info(f'Reuse reverse: {reverse}')
                    port = int(reverse.local[4:])
                else:
                    logger.info(f'Remove redundant forward: {reverse}')
                    self.__adb_forward_remove(reverse.local)

        if port:
            return port
        else:
            # Create new reverse
            port = random_port((21000, 22000))
            reverse = adbutils.ReverseItem(f'tcp:{port}', remote)
            logger.info(f'Create reverse: {reverse}')
            self.adb.reverse(reverse.local, reverse.remote)
            return port

    def __adb_forward_remove(self, local):
        """
        Equivalent to `adb -s <serial> forward --remove <local>`
        More about the commands send to ADB server, see:
        https://cs.android.com/android/platform/superproject/+/master:packages/modules/adb/SERVICES.TXT

        Args:
            local (str): Such as 'tcp:2437'
        """
        with self.adb_client._connect() as c:
            list_cmd = f"host-serial:{self.serial}:killforward:{local}"
            c.send_command(list_cmd)
            c.check_okay()

    @staticmethod
    def __load_screenshot(screenshot, method):
        if method == 0:
            pass
        elif method == 1:
            screenshot = screenshot.replace(b'\r\n', b'\n')
        elif method == 2:
            screenshot = screenshot.replace(b'\r\r\n', b'\n')
        else:
            raise Exception(f'Unknown method to load screenshots: {method}')

        # fix compatibility issues for adb screencap decode problem when the data is from vmos pro
        # When use adb screencap for a screenshot from vmos pro, there would be a header more than that from emulator
        # which would cause image decode problem. So i check and remove the header there.
        if screenshot.startswith(b'long long=8 fun*=10\n'):
            screenshot = screenshot.replace(b'long long=8 fun*=10\n', b'', 1)

        image = numpy.fromstring(screenshot, numpy.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        if image is None:
            raise OSError('Empty image')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def __process_screenshot(self, screenshot):
        for method in self.__screenshot_method_fixed:
            try:
                result = self.__load_screenshot(screenshot, method=method)
                self.__screenshot_method_fixed = [method] + self.__screenshot_method
                return result
            except OSError:
                continue

        self.__screenshot_method_fixed = self.__screenshot_method
        if len(screenshot) < 100:
            logger.warning(f'Unexpected screenshot: {screenshot}')
            raise AcceptDataError(len(screenshot))
        if len(screenshot) < 3680000:
            raise AcceptDataError(len(screenshot))
        raise OSError(f'cannot load screenshot')

    def __screen_disk(self, path):
        i = (self.project_path + path).rindex("/")
        dic_path = (self.project_path + path)[:i]
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)
        re = self.__screen_memery()
        cv2.imwrite(self.project_path + path, re)
        time.sleep(self.sleep_time)
        return self.project_path + path

    def __screen_memery(self):
        if str(self.get("device_control_method")).upper() == "ADB":
            image = self._screen_adb()
        elif str(self.get("device_control_method")).upper() == "ADB_NC":
            image = self._screen_adb_nc()
        else:
            image = None
        self.recent_img = image
        return image

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def _screen_adb(self, timeout=10, chunk_size=262144):
        cmd = ['screencap', '-p']
        cmd = list(map(str, cmd))
        stream = self.adb.shell(cmd, timeout=timeout, stream=True)
        content = recv_all(stream, chunk_size)
        image = self.__process_screenshot(content)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        return image

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def _screen_adb_nc(self, timeout=5, chunk_size=262144):
        cmd = ['screencap']
        cmd += ['|', 'nc', '127.0.0.1', 7904]
        cmd = list(map(str, cmd))
        server = self.__reverse_server()
        server.settimeout(5)
        _ = self.adb.shell(cmd, timeout=timeout, stream=True)
        try:
            # Server accept connection
            conn, conn_port = server.accept()
        except socket.timeout:
            raise adbutils.AdbTimeout('reverse server accept timeout')
        data = recv_all(conn, chunk_size=chunk_size)
        if len(data) < 100:
            logger.warning(f'Unexpected screenshot: {data}')
            raise AcceptDataError(len(data))
        if len(data) < 3680000:
            raise AcceptDataError(len(data))
        # Server close connection
        conn.close()
        # Load data
        header = numpy.frombuffer(data[0:12], dtype=numpy.uint32)
        channel = 4  # screencap sends an RGBA image
        width, height, _ = header  # Usually to be 1280, 720, 1

        image = numpy.frombuffer(data, dtype=numpy.uint8)
        shape = image.shape[0]
        image = image[shape - width * height * channel:].reshape(height, width, channel)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        return image
