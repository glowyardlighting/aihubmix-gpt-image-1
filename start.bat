@echo off
echo 🚀 启动 AIHubMix Image MCP Server
echo ================================

REM 检查 Python 是否安装
set PYTHON_PATH=C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe
if not exist "%PYTHON_PATH%" (
    echo Python 未找到在 %PYTHON_PATH%
    echo 请检查 Python 安装路径
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
"%PYTHON_PATH%" -c "import httpx" >nul 2>&1
if errorlevel 1 (
    echo 安装依赖...
    "%PYTHON_PATH%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查配置文件
if not exist ".env" (
    echo ⚠️  未找到 .env 文件
    echo 📝 请创建 .env 文件并设置 AIHUBMIX_API_KEY
    echo 示例内容：
    echo AIHUBMIX_API_KEY=your_api_key_here
    echo AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
    echo.
    pause
)

REM 启动服务器
echo 启动 MCP 服务器...
"%PYTHON_PATH%" server.py

pause