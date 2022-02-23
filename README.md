1、python 要使用3.9.X 64位
2、
cd 到项目根目录
python -m venv venv
.\venv\Scripts\activate
.\venv\scripts\python.exe -m pip install --upgrade pip
pip install .\tookit\Polygon3-3.0.9.1-cp39-cp39-win_amd64.whl
pip install .\tookit\python_Levenshtein-0.12.2-cp39-cp39-win_amd64.whl
pip install -r requirements.txt

3、修改config/config.yaml