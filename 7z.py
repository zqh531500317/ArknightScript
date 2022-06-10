import py7zr

if __name__ == '__main__':
    with py7zr.SevenZipFile('Arknight-Script.7z', 'w') as archive:
        archive.writeall('dist/Arknight-Script/')
