import subprocess
import os

basedir = os.path.dirname(os.path.abspath(''))
dir1 = basedir + '\\venv\\Scripts\\python.exe'
dir2 = basedir + "\\gui.py"
str_ff = dir1 + " " + dir2
subprocess.Popen("cd ../&" + str_ff, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
