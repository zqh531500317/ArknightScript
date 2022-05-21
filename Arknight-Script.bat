@echo off 
if "%1" == "h" goto begin 
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin 
set curdir=%~dp0
cd /d %curdir%/webapp/dist/Arknight-Script
start Arknight-Script-win_x64.exe