import re
import requests


# 根据prts网页内容获取全部干员名称并去重
def getList():
    data = requests.get('https://prts.wiki/w/干员一览').text
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
    with open(r"..\..\asset\cand_alphabet\officer.txt", "w", encoding="utf-8") as f:
        f.write(res)


getList()
