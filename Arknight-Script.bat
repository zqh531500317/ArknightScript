@echo off 
if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin 
set curdir=%~dp0
cd /d %curdir%/webapp
start dist/Arknight-Script/Arknight-Script-win_x64.exe