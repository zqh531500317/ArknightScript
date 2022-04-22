import re
import requests


# 根据prts网页内容获取全部干员名称并去重
def getList():
    data = requests.get('https://prts.wiki/w/干员一览').text
    res = re.findall("data-cn=\"(.*?)\"", data)
    str1 = ""
    for t in res:
        str1 = str1 + t
    res = ""
    for i in range(len(str1)):
        if str1[i] not in res:
            res = res + str1[i]
    with open(r"..\..\asset\cand_alphabet\officer.txt", "w", encoding="utf-8") as f:
        f.write(res)
    # 每行一
    res2 = ''
    for i in range(len(res)):
        if i == len(res) - 1:
            res2 += res[i]
        else:
            res2 += res[i] + "\n"
    with open(r"..\..\asset\cand_alphabet\officer-paddle.txt", "w", encoding="utf-8") as f:
        f.write(res2)


getList()
