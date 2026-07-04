# -*- coding: utf-8 -*-
"""
K线模拟交易系统 - 桌面应用启动器
使用本地 HTTP 服务器 + 默认浏览器，兼容 Windows 7/10/11
"""

import os
import sys
import webbrowser
import socket
import threading
import time
import atexit
import tempfile
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler


def get_app_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def run_server(port, directory):
    os.chdir(directory)

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # 静默日志

        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            super().end_headers()

    server = HTTPServer(('127.0.0.1', port), Handler)
    server.serve_forever()


def cleanup_temp_dir(tmpdir):
    try:
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)
    except Exception:
        pass


def main():
    app_dir = get_app_dir()

    # 查找 HTML 文件
    html_file = os.path.join(app_dir, 'kline_simulator.html')
    if not os.path.exists(html_file):
        html_file = os.path.join(app_dir, 'res', 'kline_simulator.html')
    if not os.path.exists(html_file):
        import tkinter.messagebox as mb
        mb.showerror('错误', f'找不到应用文件: kline_simulator.html\n\n当前目录: {app_dir}')
        sys.exit(1)

    # 复制到临时目录（避免中文路径编码问题）
    tmpdir = tempfile.mkdtemp(prefix='kline_')
    atexit.register(lambda: cleanup_temp_dir(tmpdir))
    shutil.copy2(html_file, os.path.join(tmpdir, 'index.html'))

    # 启动服务器
    port = find_free_port()
    server_thread = threading.Thread(target=run_server, args=(port, tmpdir), daemon=True)
    server_thread.start()

    # 等待服务器就绪
    time.sleep(0.5)

    # 在默认浏览器中打开
    url = f'http://127.0.0.1:{port}/index.html'
    webbrowser.open(url)

    print(f'K线模拟交易系统已启动: {url}')
    print('关闭此窗口将停止服务。')

    # 保持主线程存活
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
