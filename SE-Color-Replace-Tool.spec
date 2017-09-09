# -*- mode: python -*-

block_cipher = None


a = Analysis(['SE-Color-Replace-Tool.py'],
             pathex=['C:\\Users\\Brandon\\Desktop\\SE-Color-Replacer-master\\SE-COLOR'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SE-Color-Replace-Tool',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='app.ico')
