set curdir=%~dp0
cd /d %curdir%
cd  .\venv\ && cd  .\Scripts\
call  activate
cd ../../
call pyinstaller .\Arknight-Script.spec --noconfirm
pause
