![image](https://github.com/zqh531500317/arknight-script/blob/master/asset/demo/demo1.png)
## 一、安装

### 1、python 3.9.X 64位

### 2、

```Bash
cd 到项目根目录
python -m venv venv
.\venv\Scripts\activate
.\venv\scripts\python.exe -m pip install --upgrade pip
pip install .\tookit\Polygon3-3.0.9.1-cp39-cp39-win_amd64.whl
pip install .\tookit\python_Levenshtein-0.12.2-cp39-cp39-win_amd64.whl
pip install -r requirements.txt
```

### 3、复制config/templete.yaml为config.yaml,修改config.yaml,注意修改serial、project_path

## 二、使用

### 1、运行Arknight-Script.bat可启动图形界面

### 2、运行start_flask.bat可启动web服务，浏览器访问127.0.0.1:5000访问