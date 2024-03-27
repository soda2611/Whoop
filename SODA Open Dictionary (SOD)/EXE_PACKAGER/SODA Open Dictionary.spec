# -*- mode: python ; coding: utf-8 -*-

from kivymd import hooks_path as kivymd_hooks_path
import getpass

a = Analysis(
    ['Ui.py'],
    pathex=[],
    binaries=[],
    datas=[
        (f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\eng_to_ipa\\resources\\phones.json', 'eng_to_ipa\\resources'),
        (f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\eng_to_ipa\\resources\\CMU_dict.db', 'eng_to_ipa\\resources'),
        (f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\eng_to_ipa\\resources\\CMU_dict.json', 'eng_to_ipa\\resources')
    ],
    hiddenimports=['kivymd.icon_definitions.md_icons'],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SODA Open Dictionary',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['func\\Logo.ico'],
    version='version.rc'
)
