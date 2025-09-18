#!/bin/bash

echo "🚀 启动 AIHubMix Image MCP Server"
echo "================================"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装或不在 PATH 中"
    echo "请先安装 Python 3.7+"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖..."
if ! python3 -c "import httpx" &> /dev/null; then
    echo "📥 安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件"
    echo "📝 请创建 .env 文件并设置 AIHUBMIX_API_KEY"
    echo "示例内容："
    echo "AIHUBMIX_API_KEY=your_api_key_here"
    echo "AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1"
    echo ""
    read -p "按回车键继续..."
fi

# 使服务器可执行
chmod +x server.py

# 启动服务器
echo "🎯 启动 MCP 服务器..."
python3 server.py