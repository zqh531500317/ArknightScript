# -*- mode: python ; coding: utf-8 -*-


block_cipher = None
hiddenimports=['engineio.async_drivers.threading']
a = Analysis(['Arknight-Script.py'],
             pathex=[],
             binaries=[],
             datas=[
             ('asset','asset'),
             ('config/schedual_templete.json','config'),
             ('config/templete.yaml','config'),
             ('tookit','tookit'),
             ('webapp','webapp'),
             ('venv/label_cn.txt','cnocr'),
             ('module/stage/*.onnx','module/stage'),
             ('module/stage/*.otf','module/stage'),
             ('module/stage/*.json','module/stage'),
             ('module/stage/*.dat','module/stage'),
             ('module/stage/*.zip','module/stage'),
             ('module/stage/images/*.png','module/stage/images'),
             ('module/inventory/images/*.sh','module/inventory/images'),
             ('module/inventory/*.onnx','module/inventory'),
             ('module/inventory/*.json','module/inventory'),
             ('module/inventory/*.pth','module/inventory'),
             ('module/inventory/*.sh','module/inventory'),
             ('README.md','.'),
             ('Arknight-Script.bat','.'),

             ],
             hiddenimports=[

            ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[
             'webapp/arknight-vue',
             'webapp/bin',
             'webapp/neutralinojs.log',
             ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Arknight-Script',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Arknight-Script')
