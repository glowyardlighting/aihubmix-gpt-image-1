@echo off
echo Starting AIHubMix Image HTTP MCP Server...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM 设置环境变量
set AIHUBMIX_API_KEY=sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
set AIHUBMIX_BASE_URL=https://aihubmix.com/v1
set AIHUBMIX_MODEL=gpt-image-1
set MCP_SERVER_NAME=aihubmix-image-mcp-server
set PORT=8000
set HOST=0.0.0.0

echo Environment variables set:
echo AIHUBMIX_API_KEY=%AIHUBMIX_API_KEY%
echo AIHUBMIX_BASE_URL=%AIHUBMIX_BASE_URL%
echo AIHUBMIX_MODEL=%AIHUBMIX_MODEL%
echo PORT=%PORT%
echo HOST=%HOST%
echo.

echo Starting HTTP server on http://%HOST%:%PORT%
echo Press Ctrl+C to stop the server
echo.

REM 启动HTTP服务器
python http_server.py

pause
