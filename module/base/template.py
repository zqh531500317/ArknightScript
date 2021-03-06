import copy
import time

import cv2
import numpy as np

from module.base.control import Adb


class Template(Adb):
    def __init__(self):
        super().__init__()

    # 模板匹配 返回所有结果 自动截图  入参：匹配图片  返回：匹配的坐标
    # screen cut 是截圖   template_path 是模板圖
    def template_match_most(self, template_path, x1=0, y1=0, x2=1280, y2=720, screen_re=None, template_threshold=0.8):
        if screen_re is None:
            screen_re = self.screen(memery=True)[y1: y2, x1: x2]
            cutted_gray_img = cv2.cvtColor(screen_re, cv2.COLOR_BGR2GRAY)  # 转化成灰色
        else:
            cutted_gray_img = cv2.cvtColor(screen_re, cv2.COLOR_BGR2GRAY)  # 转化成灰色
        if isinstance(template_path, str):
            template_path = self.project_path + '/asset/template/' + template_path
            template_path = cv2.imread(template_path, 1)  # 模板小图
            template_img = cv2.cvtColor(template_path, cv2.COLOR_BGR2GRAY)

        else:
            template_path = template_path
            template_img = cv2.cvtColor(template_path, cv2.COLOR_BGR2GRAY)
        # 模板置信度
        dets = self.__template(cutted_gray_img, template_img, template_threshold)
        # count = 0
        dst = copy.deepcopy(screen_re)
        for coord in dets:
            cv2.rectangle(dst, (int(coord[0]), int(coord[1])), (int(coord[2]), int(coord[3])), (0, 0, 255), 2)
        cv2.imwrite(self.project_path + "/asset/template/cache/template_result.png", dst)

        return dets

    # 模板匹配 返回最优的一个结果 自动截图  入参：匹配图片  返回：匹配的坐标
    def template_match_best(self, template_img, x1=0, y1=0, x2=1280, y2=720, screen_re=None, template_threshold=0.8):
        dets = self.template_match_most(template_img, x1, y1, x2, y2, screen_re=screen_re,
                                        template_threshold=template_threshold)

        if len(dets) == 0:
            return dets
        res = dets[0]
        for coord in dets:
            if coord[4] > res[4]:
                res = coord
        return res

    # 判断是否成功匹配模板
    def is_template_match(self, template_img, x1=0, y1=0, x2=1280, y2=720, screen_re=None, template_threshold=0.8):
        res = self.template_match_best(template_img, x1, y1, x2, y2, screen_re=screen_re,
                                       template_threshold=template_threshold)
        return len(res) == 5

    # 用于模板匹配
    def __py_nms(self, dets, thresh):
        """Pure Python NMS baseline."""
        # x1、y1、x2、y2、以及score赋值
        # （x1、y1）（x2、y2）为box的左上和右下角标
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]
        # 每一个候选框的面积
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        # order是按照score降序排序的
        order = scores.argsort()[::-1]
        # print("order:",order)

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            # 计算当前概率最大矩形框与其他矩形框的相交框的坐标，会用到numpy的broadcast机制，得到的是向量
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            # 计算相交框的面积,注意矩形框不相交时w或h算出来会是负数，用0代替
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            # 计算重叠度IOU：重叠面积/（面积1+面积2-重叠面积）
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            # 找到重叠度不高于阈值的矩形框索引
            inds = np.where(ovr <= thresh)[0]
            # print("inds:",inds)
            # 将order序列更新，由于前面得到的矩形框索引要比矩形框在原order序列中的索引小1，所以要把这个1加回来
            order = order[inds + 1]
        return keep

    # 用于模板匹配
    def __template(self, img_gray, template_img, template_threshold):
        """
        img_gray:待检测的灰度图片格式
        template_img:模板小图，也是灰度化了
        template_threshold:模板匹配的置信度
        """

        h, w = template_img.shape[:2]
        res = cv2.matchTemplate(img_gray, template_img, cv2.TM_CCOEFF_NORMED)
        start_time = time.time()
        loc = np.where(res >= template_threshold)  # 大于模板阈值的目标坐标
        score = res[res >= template_threshold]  # 大于模板阈值的目标置信度
        # 将模板数据坐标进行处理成左上角、右下角的格式
        xmin = np.array(loc[1])
        ymin = np.array(loc[0])
        xmax = xmin + w
        ymax = ymin + h
        xmin = xmin.reshape(-1, 1)  # 变成n行1列维度
        xmax = xmax.reshape(-1, 1)  # 变成n行1列维度
        ymax = ymax.reshape(-1, 1)  # 变成n行1列维度
        ymin = ymin.reshape(-1, 1)  # 变成n行1列维度
        score = score.reshape(-1, 1)  # 变成n行1列维度
        data_hlist = [xmin, ymin, xmax, ymax, score]
        data_hstack = np.hstack(data_hlist)  # 将xmin、ymin、xmax、yamx、scores按照列进行拼接
        thresh = 0.3  # NMS里面的IOU交互比阈值
        keep_dets = self.__py_nms(data_hstack, thresh)
        # print("nms time:", time.time() - start_time)  # 打印数据处理到nms运行时间
        dets = data_hstack[keep_dets]  # 最终的nms获得的矩形框
        return dets
