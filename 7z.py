import os

import py7zr

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    os.chdir(path + "/dist")
    with py7zr.SevenZipFile(path + '/Arknight-Script.7z', 'w') as archive:
        archive.writeall('Arknight-Script/')
