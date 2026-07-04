# -*- mode: python ; coding: utf-8 -*-
"""
K线模拟交易系统 - PyInstaller 打包配置
用法: pyinstaller kline.spec
"""

import os
import sys

block_cipher = None

# 动态计算路径（兼容不同环境）
SPEC_DIR = os.path.dirname(os.path.abspath(SPECPATH)) if 'SPECPATH' in dir() else os.path.dirname(os.path.abspath(__file__))
DESKTOP_DIR = SPEC_DIR  # spec 文件在 desktop/ 目录下
SRC_DIR = os.path.join(SPEC_DIR, '..', 'src')
HTML_FILE = os.path.join(SRC_DIR, 'enhanced-v2.html')
LAUNCHER = os.path.join(DESKTOP_DIR, 'app.py')

assert os.path.exists(HTML_FILE), f"HTML not found: {HTML_FILE}"
assert os.path.exists(LAUNCHER), f"Launcher not found: {LAUNCHER}"

# 构建时将 HTML 复制到 spec 所在目录
import shutil
shutil.copy2(HTML_FILE, os.path.join(DESKTOP_DIR, 'kline_simulator.html'))

a = Analysis(
    [LAUNCHER],
    pathex=[DESKTOP_DIR],
    binaries=[],
    datas=[(os.path.join(DESKTOP_DIR, 'kline_simulator.html'), '.')],
    hiddenimports=[
        'webview',
        'webview.platforms.winforms',
        'webview.platforms.edgechromium',
        'webview.js.css',
        'clr_loader',
        'pythonnet',
        'http.server',
        'webbrowser',
        'tkinter',
        'tkinter.messagebox',
        'threading',
        'socket',
        'json',
        'traceback',
        'tempfile',
        'shutil',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'PIL', 'cv2', 'scipy', 'tensorflow', 'torch'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name='K线模拟交易系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
