#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
K线模拟交易系统 - 打包构建脚本
使用 PyInstaller 将桌面应用打包为独立 EXE 文件

用法:
    python build.py              # 使用默认 spec 构建
    python build.py --console    # 构建带控制台窗口的版本（调试用）
    python build.py --clean      # 清理构建缓存后重新构建
"""

import os
import sys
import shutil
import argparse


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DESKTOP_DIR = os.path.join(ROOT_DIR, 'desktop')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'dist')
BUILD_DIR = os.path.join(ROOT_DIR, 'build')

# 打包入口文件
APP_SCRIPT = os.path.join(DESKTOP_DIR, 'app.py')
# HTML 资源文件
HTML_FILE = os.path.join(ROOT_DIR, 'src', 'enhanced-v2.html')
# 输出 EXE 名称
EXE_NAME = 'K线模拟交易系统'


def check_prerequisites():
    """检查前置条件"""
    errors = []

    if not os.path.exists(APP_SCRIPT):
        errors.append(f'入口脚本不存在: {APP_SCRIPT}')
    if not os.path.exists(HTML_FILE):
        errors.append(f'HTML 文件不存在: {HTML_FILE}')

    try:
        import PyInstaller
    except ImportError:
        errors.append('PyInstaller 未安装，请执行: pip install pyinstaller')

    if errors:
        print('[ERROR] 前置条件检查失败:')
        for e in errors:
            print(f'  - {e}')
        sys.exit(1)

    print('[OK] 前置条件检查通过')


def clean():
    """清理构建缓存"""
    for d in [BUILD_DIR, OUTPUT_DIR]:
        if os.path.exists(d):
            print(f'[CLEAN] 删除 {d}')
            shutil.rmtree(d, ignore_errors=True)

    # 清理 .spec 自动生成的文件
    for f in os.listdir(ROOT_DIR):
        if f.endswith('.spec'):
            os.remove(os.path.join(ROOT_DIR, f))


def build(console=False):
    """执行 PyInstaller 构建"""
    import PyInstaller.__main__

    # 确保 HTML 文件复制到 desktop 目录供打包使用
    target_html = os.path.join(DESKTOP_DIR, 'kline_simulator.html')
    shutil.copy2(HTML_FILE, target_html)
    print(f'[COPY] {HTML_FILE} -> {target_html}')

    # 构建参数
    args = [
        APP_SCRIPT,
        '--name', EXE_NAME,
        '--onefile',
        '--noconfirm',
        f'--distpath={OUTPUT_DIR}',
        f'--workpath={BUILD_DIR}',
        f'--add-data={target_html};.',
        '--hidden-import=webview',
        '--hidden-import=webview.platforms.winforms',
        '--hidden-import=webview.platforms.edgechromium',
        '--hidden-import=webview.js.css',
        '--hidden-import=clr_loader',
        '--hidden-import=pythonnet',
        '--hidden-import=http.server',
        '--hidden-import=webbrowser',
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.messagebox',
        '--hidden-import=threading',
        '--hidden-import=socket',
        '--hidden-import=json',
        '--hidden-import=traceback',
        '--hidden-import=tempfile',
        '--hidden-import=shutil',
        '--target-arch=x86_64',
        '--exclude-module=matplotlib',
        '--exclude-module=numpy',
        '--exclude-module=pandas',
        '--exclude-module=PIL',
        '--exclude-module=cv2',
        '--exclude-module=scipy',
        '--exclude-module=tensorflow',
        '--exclude-module=torch',
    ]

    if not console:
        args.append('--windowed')

    print(f'\n[BUILD] 开始打包 {EXE_NAME}.exe ...')
    print(f'[BUILD] 参数: {" ".join(args)}\n')

    PyInstaller.__main__.run(args)

    # 清理临时 HTML
    if os.path.exists(target_html):
        os.remove(target_html)

    exe_path = os.path.join(OUTPUT_DIR, f'{EXE_NAME}.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f'\n[SUCCESS] 构建完成: {exe_path}')
        print(f'[SUCCESS] 文件大小: {size_mb:.1f} MB')
    else:
        print(f'\n[ERROR] 构建失败，未找到输出文件')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='K线模拟交易系统 - 打包构建脚本')
    parser.add_argument('--console', action='store_true', help='构建带控制台窗口的版本（调试用）')
    parser.add_argument('--clean', action='store_true', help='清理构建缓存后重新构建')
    args = parser.parse_args()

    check_prerequisites()

    if args.clean:
        clean()

    build(console=args.console)


if __name__ == '__main__':
    main()
