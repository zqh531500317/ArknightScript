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


class CoreConfig:

    def __init__(self):
        logger.info("初始化配置文件类")
        self.project_path = project_root_path()
        self.screen_path = self.project_path + '/cache/screen.png'
        self.configList = {}
        self.read()
        self.serial = self.configList["Config"]["Emulator"]["serial"]
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

    @staticmethod
    def read_json(path):
        with open(path, 'r', encoding='utf-8') as load_f:
            schedual_dict = json.load(load_f, object_pairs_hook=OrderedDict)
        return schedual_dict

    @staticmethod
    def write_json(load_dict, path):
        with open(path, "w", encoding='utf-8') as dump_f:
            json.dump(load_dict, dump_f, ensure_ascii=False, indent=2)


cf = CoreConfig()
configList = cf.configList
project_path = cf.project_path
compared_path = screen_path = cf.screen_path
endFight_path = project_path + "/asset/template/cache/endFight.png"
sleep_time = cf.configList["Config"]["Screen"]["time"]
device_control_method = cf.configList["Config"]["Emulator"]["device_control_method"]
device_screenshot_method = cf.configList["Config"]["Emulator"]["device_screenshot_method"]
timeout_time = 60 * 20
timeout_time_max = 60 * 60
with open(project_path + "/asset/cand_alphabet/officer.txt", "r", encoding='utf-8') as f:
    cand_alphabet_officer = f.read()
