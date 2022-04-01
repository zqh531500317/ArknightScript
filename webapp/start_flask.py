import os

basedir = os.path.dirname(os.path.abspath(''))
if os.path.isdir(basedir + "/cv2"):
    file = open('test.txt', 'w')
    dir2 = basedir + "\\Arknight-Script.exe"
    str_ff = dir2
    file.write("cd ../&" + str_ff)
    file.close()
    os.system(str_ff)
else:
    file = open('test.txt', 'w')
    dir1 = basedir + '\\venv\\Scripts\\python.exe'
    dir2 = basedir + "\\Arknight-Script.py"
    str_ff = dir1 + " " + dir2
    file.write("cd ../&" + str_ff)
    file.close()
    os.system(str_ff)
