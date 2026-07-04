# -*- coding: utf-8 -*-
"""
K线模拟交易系统 v2.0 - 桌面应用启动器
基于 pywebview (Edge WebView2)，提供原生窗口体验
兼容: Windows 7 SP1 x64 / Windows 10 x64 / Windows 11 x64

Win7 用户需安装 Microsoft Edge WebView2 Runtime:
  https://go.microsoft.com/fwlink/p/?LinkId=2124703
"""

import os
import sys
import json
import traceback

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def find_html():
    candidates = [
        os.path.join(get_app_dir(), 'kline_simulator.html'),
        os.path.join(get_app_dir(), 'res', 'kline_simulator.html'),
        # 开发模式：相对于 desktop/ 目录的 src/enhanced-v2.html
        os.path.join(get_app_dir(), '..', 'src', 'enhanced-v2.html'),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def fallback_browser(html_path):
    """当 WebView2 不可用时，降级使用默认浏览器"""
    import webbrowser
    import tempfile
    import shutil
    import socket
    import threading
    import time
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    tmpdir = tempfile.mkdtemp(prefix='kline_')
    shutil.copy2(html_path, os.path.join(tmpdir, 'index.html'))
    os.chdir(tmpdir)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]

    class Handler(SimpleHTTPRequestHandler):
        def log_message(self, f, *a): pass

    def serve():
        HTTPServer(('127.0.0.1', port), Handler).serve_forever()

    threading.Thread(target=serve, daemon=True).start()
    time.sleep(0.3)
    webbrowser.open(f'http://127.0.0.1:{port}/index.html')

    import tkinter.messagebox as mb
    mb.showinfo(
        'K线模拟交易系统',
        '已通过浏览器打开。\n\n'
        '如需原生窗口体验，请安装 Microsoft Edge WebView2 Runtime:\n'
        'https://go.microsoft.com/fwlink/p/?LinkId=2124703\n\n'
        '关闭浏览器页面后，请手动关闭此窗口。'
    )


def main():
    html_path = find_html()
    if html_path is None:
        import tkinter.messagebox as mb
        mb.showerror('错误', '找不到应用文件 kline_simulator.html')
        sys.exit(1)

    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    try:
        import webview

        # 检测 WebView2 是否可用
        webview_available = True
        try:
            # 尝试验证 edgechromium gui
            pass
        except Exception:
            webview_available = False

        if webview_available:
            # 尝试使用 edgechromium 后端
            window = webview.create_window(
                title='K线模拟交易系统 v2.0',
                html=html,
                width=1320,
                height=820,
                min_size=(960, 600),
                resizable=True,
                text_select=False,
            )

            try:
                webview.start(gui='edgechromium', http_server=True)
            except Exception as e:
                # edgechromium 不可用，尝试 mshtml 或降级
                try:
                    webview.start(gui='mshtml', http_server=True)
                except Exception:
                    raise e
        else:
            raise RuntimeError('WebView2 not available')

    except Exception as e:
        # pywebview 失败，降级使用浏览器
        print(f'[Warning] pywebview 启动失败: {e}')
        traceback.print_exc()
        fallback_browser(html_path)

    # 如果 pywebview 正常退出
    sys.exit(0)


if __name__ == '__main__':
    main()
