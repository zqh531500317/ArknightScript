set curdir=%~dp0
cd /d %curdir%
set FLASK_APP=Arknight-Script.py
start venv/Scripts/python.exe -m flask run --host 0.0.0.0