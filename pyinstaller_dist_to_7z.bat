echo ������汾��(����1.1.0)
set /p version=
echo %version%
echo ���������˵��
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
