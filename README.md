![image](https://github.com/zqh531500317/arknight-script/blob/master/asset/demo/demo1.png)
# 一、安装
## 方案(1)手动安装 
### 1、环境要求python 3.9.X 64位

### 2、

```Bash
git clone https://github.com/zqh531500317/arknight-script.git
cd arknight-script
python -m venv venv
.\venv\Scripts\activate
.\venv\scripts\python.exe -m pip install --upgrade pip
pip install .\tookit\Polygon3-3.0.9.1-cp39-cp39-win_amd64.whl
pip install .\tookit\python_Levenshtein-0.12.2-cp39-cp39-win_amd64.whl
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
## 方案(2)下载可执行程序 
### 下载 Arknight Script CLI

## 二、使用

### 1、调整模拟器分辨率为1280*720，确保模拟器已启动
### 2、
####复制config/templete.yaml为config.yaml,修改config.yaml,注意修改serial、project_path
####要使用基建换班，则复制config/schedual_templete.json为schedual.json，修改文件内容

### 3、对于手动安装：
####运行Arknight-Script.bat可启动图形界面
####运行start_flask.bat可启动web服务，浏览器访问127.0.0.1:5000访问
### 4、对于下载可执行程序 ： 
####Arknight-Script.exe可启动web服务，浏览器访问127.0.0.1:5000访问
####.bat可启动图形界面
