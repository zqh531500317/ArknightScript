import os

basedir = os.path.dirname(os.path.abspath(''))
if os.path.isdir(basedir + "/cv2"):
    file = open('test.txt', 'w')
    dir2 = basedir + "\\Arknight-Script.exe"
    str_ff = dir2
    file.write("cd ../&" + str_ff)
    file.close()
    os.system("cd ../&" + str_ff)
else:
    file = open('test.txt', 'w')

    dir1 = basedir + '\\venv\\Scripts\\python.exe '
    str_ff = "-m flask run --host 0.0.0.0"
    cmd = "cd ../&set FLASK_APP=Arknight-Script.py&" + dir1 + str_ff
    file.write(cmd)
    file.close()
    os.system(cmd)
