import re


# 根据prts网页内容获取全部干员名称并去重
def getList():
    with open("d:/1.txt", "r", encoding='utf-8') as f:
        data = f.read()  # 读取文件
    res = re.findall("data-cn=\"(.*?)\"", data)
    str = ""
    for t in res:
        str = str + t
    print(str)
    res = ""
    for i in range(len(str)):
        if (str[i] not in res):
            res = res + str[i]

    print(res)

