@echo off
chcp 65001 >nul
title K线模拟交易系统 - 构建脚本

echo ============================================
echo   K线模拟交易系统 - 打包构建
echo ============================================
echo.

:: 检查 Python 是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未检测到 Python，请先安装 Python 3.8+
    echo         下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 显示 Python 版本
echo [INFO] Python 版本:
python --version
echo.

:: 安装依赖
echo [INFO] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] 依赖安装失败
    pause
    exit /b 1
)
echo.

:: 执行构建
echo [INFO] 开始构建 EXE...
python build.py %*
echo.

if %errorlevel% equ 0 (
    echo ============================================
    echo   构建成功！
    echo   输出文件: dist\K线模拟交易系统.exe
    echo ============================================
) else (
    echo ============================================
    echo   构建失败，请检查错误信息
    echo ============================================
)

pause
