# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainScript.py'],
    pathex=[],
    binaries=[('en_core_web_md' , 'en_core_web_md'),
    ('/opt/homebrew/Cellar/tesseract/5.3.3/bin/tesseract' , 'tesseract'),
    ('poppler' , 'poppler')],
    datas=[('logo.png' , '.'),
    ('folder.png' , '.'),
    ('background2.jpg' , '.'),
    ('wireless_splash.png' , '.'),
    ('rename_logo2.png' , '.'),
    ('screenshot_drag.png' , '.'),
    ('screenshot_export.png' , '.')],
    hiddenimports=[],
    hookspath=[],
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
    name='mainScript',
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
)
app = BUNDLE(
    exe,
    name='ReNAME.app',
    icon='logo2.icns',
    bundle_identifier=None,
)
