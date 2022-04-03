from PIL import Image
import numpy as np
from module.utils.core_control import *


# 展示图片
def show(region):
    cv2.imshow('image', region)
    cv2.waitKey(0)


# 从磁盘图片读取到内存
def read(uri):
    return cv2.imread(uri)


# 裁剪图片  只保留(x1,y1) (x2,y2)之间的矩形区域
def cut(region, x1, y1, x2, y2):
    cropped = region[y1: y2, x1:x2]
    return cropped


# 裁剪图片  只保留(x1,y1) (x2,y2)之间的矩形区域
def cut_by_path(path, x1, y1, x2, y2):
    region = read(path)
    cropped = region[y1: y2, x1:x2]
    return cropped


# 从内存保存图片到磁盘
def write(uri, region):
    cv2.imwrite(uri, region)


# 获取像素点的rgb值
def getRGB(x, y, img_path=cf.screen_path):
    image = Image.open(img_path)
    return image.getpixel((x, y))[:3]


# 均值哈希算法
def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 差值哈希算法
def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 感知哈希算法
def pHash(img):
    # 缩放32*32
    img = cv2.resize(img, (32, 32))  # , interpolation=cv2.INTER_CUBIC

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # opencv实现的掩码操作
    dct_roi = dct[0:8, 0:8]

    hash = []
    avreage = np.mean(dct_roi)
    for i in range(dct_roi.shape[0]):
        for j in range(dct_roi.shape[1]):
            if dct_roi[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash


# 灰度直方图算法
def calculate(image1, image2):
    # 计算单通道的直方图的相似值
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                     (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


# RGB每个通道的直方图相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    return sub_data


# Hash值对比
def cmpHash(hash1, hash2):
    # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
    # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
    # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


# 比较图片部分区域纯白像素点(255,255,255)完全是否相同
def compareAllWhile(name):
    screen()
    obj = ui[name]
    templete_path = obj["file"]
    x1 = obj["area"][0]
    y1 = obj["area"][1]
    x2 = obj["area"][2]
    y2 = obj["area"][3]
    flag = True
    image1 = Image.open(templete_path)
    image2 = Image.open(cf.screen_path)
    for x in range(x1, x2):
        for y in range(y1, y2):
            data1 = image1.getpixel((x, y))[:3]
            data2 = image2.getpixel((x, y))[:3]
            if data1[0] == 255 and data1[1] == 255 and data1[2] == 255:
                if data2[0] != 255 or data2[1] != 255 or data2[2] != 255:
                    flag = False

    return flag


# 比较图片子区域是否完全相同
def compareSame(name):
    obj = ui[name]
    templete_path = obj["file"]
    x1 = obj["area"][0]
    y1 = obj["area"][1]
    x2 = obj["area"][2]
    y2 = obj["area"][3]
    image1 = cv2.imread(templete_path)[y1: y2, x1: x2]
    image2 = screen(memery=True)[y1: y2, x1: x2]
    # cv2.imwrite("image1.jpg", image1)
    # cv2.imwrite("image2.jpg", image2)
    difference = cv2.subtract(image1, image2)

    result = not np.any(difference)

    if result is True:
        logger.debug("与图片%s完全相同", templete_path)
    else:
        logger.debug("与图片%s不相同", templete_path)
    return result


# 比较图片子区域是否相似 返回相似度0<=n<=1
def compareSimilar(name):
    obj = ui[name]
    templete_path = obj["file"]
    x1 = obj["area"][0]
    y1 = obj["area"][1]
    x2 = obj["area"][2]
    y2 = obj["area"][3]
    image1 = cv2.imread(templete_path)[y1: y2, x1: x2]
    image2 = screen(memery=True)[y1: y2, x1: x2]
    # cv2.imwrite("image1.jpg", image1)
    # cv2.imwrite("image2.jpg", image2)

    n = classify_hist_with_split(image1, image2)
    logger.debug("与图片%s相似度为%s", templete_path, n)
    return n
