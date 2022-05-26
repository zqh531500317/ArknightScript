import collections
import os
import time
import cv2
from module.base.config import CoreConfig
from module.base.state import State
from logzero import logger


class Store(CoreConfig):
    # key:running_job.id value:[imglist]
    img_store = collections.defaultdict()

    def __init__(self):
        super().__init__()
        self.state = State()

    def store_add_img(self, img):
        job_id = self.state.running_job["id"]
        if (job_id == "") or (not self.debug):
            return
        # 压缩图片
        x, y = img.shape[0:2]
        temp = cv2.resize(img, (int(y / 2), int(x / 2)))
        # 添加图片
        store = self.img_store.get(job_id)
        if store is None:
            self.img_store[job_id] = []
            path = self.project_path + "/screenshots/debug/{}/{}".format(str(job_id), str(int(time.time_ns() / 1000)))
            if not os.path.exists(path):
                os.makedirs(path)
            self.img_store[job_id].append(path)
        self.img_store[job_id].append(
            ["/" + str(time.time_ns()) + ".jpg", temp]
        )

    def store_save_imgs(self):
        job_id = self.state.running_job["id"]
        if (job_id == "") or (not self.debug):
            return
        logger.info("debug_recode 开始存储记录")
        i = 0
        temp = self.img_store.pop(job_id)
        path = temp[0]
        for img in temp[1:]:
            cv2.imwrite(path + img[0], img[1])
            i += 1
        logger.info("总共存储照片%s张,存储至/screenshots/debug/%s/%s", i, str(job_id), str(int(time.time_ns() / 1000)))
        logger.info("debug_recode 存储记录完毕")
