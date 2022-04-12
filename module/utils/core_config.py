import shutil
import yaml
import os
import psutil
import sys
import json
from collections import OrderedDict
from logzero import logger
from module.utils.core_utils import project_root_path
from module.utils.core_decoratir import debug_recode, timer, bench_time, singleton
from func_timeout import func_set_timeout


@singleton
class CoreConfig:
    def __init__(self):
        logger.info("初始化配置文件类")
        config = self.project_path + '/config/config.yaml'
        templete = self.project_path + '/config/templete.yaml'
        if not os.path.exists(config):
            shutil.copy(templete, config)
            logger.info("file config.yaml not exist,copy templete.yaml=>config.yaml")
        self.configList = {}
        self.read()
        # 判断程序是否正在运行
        pid = self.configList["Config"]["System"]["pid"]
        if pid is not None:
            pid = int(pid)
            for process in psutil.process_iter():
                if process.pid == pid and process.name == 'python.exe':
                    print("进程{}正在运行，退出本程序".format(pid))
                    sys.exit()
        self.write("project_path", self.project_path)
        self.write("pid", os.getpid())
        self.timeout_time = 60 * 20
        self.timeout_time_max = 60 * 60
        with open(self.project_path + "/asset/cand_alphabet/officer.txt", "r", encoding='utf-8') as f:
            self.cand_alphabet_officer = f.read()
        self.recruit_tag = "医疗干员远程位治新手高级资深近战先锋狙击" \
                           "术师卫重装辅助特种支援输出群攻减速生存防护削弱" \
                           "移控场爆发召唤快复活费用回机械"
        self.number_tag = "1234567890/"
        self.ziyuanshouji_tag = "空中威胁资源保障粉碎防御货物运送战术演习固若金汤势不可挡摧枯拉朽身先士卒"

    def read(self):
        # 直接打开读取
        f = open(self.project_path + '/config/config.yaml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        # 转换成字典读出来
        self.configList = yaml.load(result, Loader=yaml.FullLoader)
        logger.debug("load config.yaml")

    def write(self, key, value):
        logger.debug("alter config.yaml %s -->  %s", key, value)
        path = self.project_path + '/config/config.yaml'
        with open(path, 'r', encoding='utf-8') as f:
            lines = []  # 创建了一个空列表，里面没有元素
            for line in f.readlines():
                if line != '\n':
                    lines.append(line)
            f.close()
        with open(path, 'w', encoding='utf-8') as f:
            flag = 0
            for line in lines:
                if key in line and '#' not in line:
                    leftstr = line.split(":")[0]
                    newline = "{0}: {1}".format(leftstr, value)
                    line = newline
                    f.write('%s\n' % line)
                    flag = 1
                else:
                    f.write('%s' % line)
            f.close()
            return flag

    # 查找单个键
    def get(self, target) -> str:
        queue = [self.configList]
        while len(queue) > 0:
            data = queue.pop()
            for key, value in data.items():
                if key == target:
                    return value
                elif type(value) == dict:
                    queue.append(value)
        return ""

    @staticmethod
    def read_json(path):
        with open(path, 'r', encoding='utf-8') as load_f:
            schedual_dict = json.load(load_f, object_pairs_hook=OrderedDict)
        return schedual_dict

    @staticmethod
    def write_json(load_dict, path):
        with open(path, "w", encoding='utf-8') as dump_f:
            json.dump(load_dict, dump_f, ensure_ascii=False, indent=2)

    @property
    def project_path(self):
        return project_root_path()

    @property
    def screen_path(self):
        return self.project_path + '/cache/screen.png'

    @property
    def compared_path(self):
        return self.screen_path

    @property
    def endFight_path(self):
        return self.project_path + "/asset/template/cache/endFight.png"

    @property
    def serial(self):
        return self.get("serial")

    @property
    def sleep_time(self):
        return self.get("sleep_time")

    @property
    def device_control_method(self):
        return self.get("device_control_method")

    @property
    def device_screenshot_method(self):
        return self.get("device_screenshot_method")

    @property
    def activity_name(self):
        return self.get("activity_name")

    @property
    def package_name(self):
        return self.get("package_name")

    @property
    def enable_mail(self):
        return self.get("enable_mail")

    @property
    def sender(self):
        return self.get("sender")

    @property
    def authorization(self):
        return self.get("authorization")

    @property
    def host(self):
        return self.get("host")

    @property
    def receiver(self):
        return self.get("receiver")
    @property
    def xinpian_1(self):
        return self.get("xinpian_1")
    @property
    def xinpian_2(self):
        return self.get("xinpian_2")


cf = CoreConfig()
configList = cf.configList
project_path = cf.project_path
compared_path = screen_path = cf.screen_path
endFight_path = project_path + "/asset/template/cache/endFight.png"
sleep_time = cf.configList["Config"]["Screen"]["sleep_time"]
device_control_method = cf.configList["Config"]["Emulator"]["device_control_method"]
device_screenshot_method = cf.configList["Config"]["Emulator"]["device_screenshot_method"]
timeout_time = 60 * 20
timeout_time_max = 60 * 60
with open(project_path + "/asset/cand_alphabet/officer.txt", "r", encoding='utf-8') as f:
    cand_alphabet_officer = f.read()
