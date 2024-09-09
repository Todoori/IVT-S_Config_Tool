# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['IVTConfig.py'],
    pathex=['C:\\Users\\jmh-adm\\Documents\\Sciebo\\04_PythonScripte\\ivt-s_configtool\\src\\Lib\\site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=['can', 'can.interfaces.pcan'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IVTConfig',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IVTConfig',
)
