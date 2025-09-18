@echo off
echo 启动 AIHubMix Image MCP Server (图像生成已禁用)
echo.

REM 设置环境变量
set AIHUBMIX_API_KEY=sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
set AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
set AIHUBMIX_MODEL=dall-e-3
set MCP_SERVER_NAME=aihubmix-image-mcp-server
set ENABLE_IMAGE_GENERATION=false

echo 环境变量已设置:
echo   AIHUBMIX_API_KEY: %AIHUBMIX_API_KEY%
echo   AIHUBMIX_BASE_URL: %AIHUBMIX_BASE_URL%
echo   ENABLE_IMAGE_GENERATION: %ENABLE_IMAGE_GENERATION%
echo.

echo 启动服务器...
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe server.py

pause
