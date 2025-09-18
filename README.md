# AIHubMix Image Generation MCP Server

一个基于 Model Context Protocol (MCP) 的图像生成服务器，使用 AIHubMix API 来访问 OpenAI 的图像生成模型。兼容 Claude Code 和其他 MCP 客户端。

## 功能特性

- 🎨 使用 AIHubMix API 访问 OpenAI 的 DALL-E 模型
- 🖼️ 支持多种图像尺寸和质量设置
- 🔧 多种 API 密钥配置方法
- 💾 自动保存生成的图像到 `images/` 文件夹
- 🛡️ 完善的错误处理和验证
- 📝 详细的生成日志和状态信息

## 支持的模型

- **DALL-E 3**: 高质量图像生成，支持多种尺寸和风格
- **DALL-E 2**: 经典图像生成模型

## 安装

1. 克隆此仓库：
```bash
git clone <repository-url>
cd aihubmix-image-mcp-server
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置您的 AIHubMix API 密钥（见配置部分）

## 配置

服务器支持多种方法来配置您的 AIHubMix API 密钥：

### 方法 1: 环境变量（推荐）

```bash
export AIHUBMIX_API_KEY="your_aihubmix_api_key_here"
export AIHUBMIX_BASE_URL="https://api.aihubmix.com/v1"
```

### 方法 2: .env 文件

在服务器目录中创建 `.env` 文件：

```env
AIHUBMIX_API_KEY=your_aihubmix_api_key_here
AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
```

### 方法 3: 配置文件

创建 `~/.config/aihubmix-image-mcp/config.json`：

```json
{
  "aihubmix_api_key": "your_aihubmix_api_key_here",
  "aihubmix_base_url": "https://api.aihubmix.com/v1"
}
```

或在服务器目录中创建本地 `config.json` 文件。

## 在 Claude Code 中使用

将此 MCP 服务器添加到 Claude Code：

```bash
# 使服务器可执行
chmod +x server.py

# 添加到 Claude Code（替换为您的实际路径）
claude mcp add-json --scope user aihubmix-image '{
  "command": "python3",
  "args": ["/path/to/aihubmix-image-mcp-server/server.py"],
  "env": {
    "AIHUBMIX_API_KEY": "your_aihubmix_api_key_here"
  }
}'

# 验证连接
claude mcp list
```

## 获取 AIHubMix API 密钥

1. 访问 [AIHubMix 官网](https://aihubmix.com)
2. 注册账户或登录
3. 在控制台中生成新的 API 密钥
4. 确保账户有足够的额度用于图像生成

### 当前配置

您的 API 配置已经设置完成：
- **API 地址**: https://aihubmix.com/v1
- **API 密钥**: sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2

配置文件已保存在 `.env` 文件中，可以直接使用。

## 工具

### generate_image

使用 AIHubMix API 生成图像。

**参数：**

- `prompt`（必需）：描述要生成图像的详细提示词
- `model`（可选）：图像生成模型 - "dall-e-3" 或 "dall-e-2"（默认："dall-e-3"）
- `size`（可选）：图像尺寸 - "1024x1024"、"1792x1024" 或 "1024x1792"（默认："1024x1024"）
- `quality`（可选）：图像质量 - "standard" 或 "hd"（默认："standard"，仅 DALL-E 3 支持）
- `style`（可选）：图像风格 - "vivid" 或 "natural"（默认："vivid"，仅 DALL-E 3 支持）
- `n`（可选）：生成图像的数量，1-4（默认：1）
- `filename`（可选）：保存图像的文件名（不含扩展名，默认："generated_image"）

**返回：**

- 文本描述生成结果
- 自动保存的图像文件到 `images/` 文件夹
- 图像 URL 和优化后的提示词

**在 Claude Code 中的示例：**

```
生成一张宁静的山景日落图像，有水晶般清澈的湖泊，保存为 mountain_sunset.png
```

## 直接运行

### HTTP 服务器（推荐用于 Smithery AI 部署）

```bash
python http_server.py
```

服务器将在 http://localhost:8000 启动，支持 HTTP MCP 协议。

### Stdio 服务器（用于本地开发）

```bash
python server.py
```

服务器通过 stdio 监听 MCP 协议消息。

## API 参考

此服务器通过 AIHubMix API 实现 OpenAI 的图像生成 API：

```bash
curl -X POST "https://api.aihubmix.com/v1/images/generations" \
    -H "Authorization: Bearer $AIHUBMIX_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "dall-e-3",
        "prompt": "your detailed prompt here",
        "size": "1024x1024",
        "quality": "standard",
        "style": "vivid"
    }'
```

## 错误处理

服务器处理各种条件：

- 缺少/无效的 API 密钥，提供有用的配置指导
- 无效的提示词和参数
- API 速率限制和网络超时
- 账户余额不足

## 故障排除

### "AIHubMix API key not found" 错误

使用上述方法之一配置您的 API 密钥。服务器按以下顺序检查：

1. `AIHUBMIX_API_KEY` 环境变量
2. 服务器目录中的 `.env` 文件
3. `~/.config/aihubmix-image-mcp/config.json` 或 `./config.json` 中的配置文件

### 权限错误

```bash
chmod +x server.py
```

### 模块导入错误

```bash
pip install -r requirements.txt
```

### 网络连接问题

- 检查网络连接
- 验证 AIHubMix API 服务状态
- 确认 API 密钥有效且有足够余额

## 依赖要求

- Python 3.7+
- AIHubMix API 密钥
- 依赖项：`httpx`、`python-dotenv`

## 贡献

欢迎贡献！此项目设计用于在 Smithery.ai 上发布。

## 许可证

MIT 许可证

## 关于

AIHubMix Image Generation MCP Server - 使用 AIHubMix API 访问 OpenAI 图像生成模型的 Model Context Protocol (MCP) 兼容服务器

## 更新日志

### v1.0.0
- 初始版本
- 支持 DALL-E 3 和 DALL-E 2 模型
- 多种配置方法
- 自动图像保存
- 完善的错误处理