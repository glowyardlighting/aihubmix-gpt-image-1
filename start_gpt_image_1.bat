@echo off
echo 启动 AIHubMix Image MCP Server (使用 gpt-image-1 模型)
echo.

REM 设置环境变量
set AIHUBMIX_API_KEY=sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
set AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
set AIHUBMIX_MODEL=gpt-image-1
set MCP_SERVER_NAME=aihubmix-image-mcp-server

echo 环境变量已设置:
echo   AIHUBMIX_API_KEY: %AIHUBMIX_API_KEY%
echo   AIHUBMIX_BASE_URL: %AIHUBMIX_BASE_URL%
echo   AIHUBMIX_MODEL: %AIHUBMIX_MODEL%
echo.

echo 启动服务器...
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe server.py

pause
