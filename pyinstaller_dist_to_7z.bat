echo 请输入版本号(例如1.1.0)
set /p version=
echo %version%
echo 请输入更新说明
set /p readme=
echo %readme%
md backup\v%version%
cd dist
Bandizip.exe c -storeroot:yes -l:5  ..\backup\v%version%\Arknight-Script-v%version%.7z Arknight-Script\
cd ..\
cd backup
cd v%version%
echo=>readme.txt
echo %readme% >> readme.txt
