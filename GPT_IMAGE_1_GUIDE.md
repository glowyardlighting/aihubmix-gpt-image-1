# GPT-Image-1 模型支持指南

## 概述

AIHubMix Image MCP Server 现在支持使用 `gpt-image-1` 模型进行图像生成，这是除了 DALL-E 2 和 DALL-E 3 之外的另一个选择。

## 主要特性

### GPT-Image-1 模型特点
- **响应格式**: 使用 base64 编码返回图像数据，而不是 URL
- **模型标识**: `gpt-image-1`
- **支持尺寸**: 256x256, 512x512, 1024x1024, 1792x1024, 1024x1792
- **图像数量**: 1-10 张
- **自动保存**: 自动解码 base64 数据并保存为 PNG 文件

### 与 DALL-E 模型的区别
| 特性 | GPT-Image-1 | DALL-E 2/3 |
|------|-------------|------------|
| 响应格式 | base64 编码 | URL 链接 |
| 质量参数 | 不支持 | 支持 (DALL-E 3) |
| 风格参数 | 不支持 | 支持 (DALL-E 3) |
| 下载方式 | 直接解码保存 | 需要下载 URL |

## 配置方法

### 方法 1: 环境变量（推荐）

```bash
set AIHUBMIX_MODEL=gpt-image-1
```

### 方法 2: 使用专用启动脚本

直接运行 `start_gpt_image_1.bat` 文件：

```cmd
start_gpt_image_1.bat
```

### 方法 3: 手动设置所有环境变量

```cmd
set AIHUBMIX_API_KEY=sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
set AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
set AIHUBMIX_MODEL=gpt-image-1
set MCP_SERVER_NAME=aihubmix-image-mcp-server
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe server.py
```

## 使用方法

### 在 Claude Code 中使用

配置 MCP 服务器时，确保设置正确的模型：

```json
{
  "mcpServers": {
    "aihubmix-image": {
      "command": "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python38\\python.exe",
      "args": ["C:\\Users\\admin\\Desktop\\aihubmix-image-mcp-server\\server.py"],
      "env": {
        "AIHUBMIX_API_KEY": "sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2",
        "AIHUBMIX_BASE_URL": "https://api.aihubmix.com/v1",
        "AIHUBMIX_MODEL": "gpt-image-1"
      }
    }
  }
}
```

### 生成图像示例

```
生成一张 solar cat lights 的图片，使用 gpt-image-1 模型
```

## 技术实现

### 请求格式
```json
{
  "model": "gpt-image-1",
  "prompt": "your prompt here",
  "size": "1024x1024",
  "n": 1,
  "response_format": "b64_json"
}
```

### 响应处理
服务器会自动：
1. 检测 `b64_json` 响应格式
2. 解码 base64 图像数据
3. 保存为 PNG 文件到 `images/` 目录
4. 返回保存路径信息

## 文件结构

```
aihubmix-image-mcp-server/
├── server.py                    # 主服务器文件
├── start_gpt_image_1.bat       # GPT-Image-1 启动脚本
├── config_gpt_image_1.env      # GPT-Image-1 配置文件
├── test_server_gpt_image_1.py  # 服务器测试脚本
├── images/                     # 生成的图片保存目录
│   ├── gpt_image_1_test.png    # 示例图片
│   └── ...
└── GPT_IMAGE_1_GUIDE.md        # 本指南
```

## 故障排除

### 常见问题

1. **网络连接问题**
   - 检查网络连接
   - 验证 AIHubMix API 服务状态
   - 确认 API 密钥有效

2. **模型不支持**
   - 确保使用正确的模型名称 `gpt-image-1`
   - 检查 API 密钥是否有权限使用该模型

3. **图像保存失败**
   - 检查 `images/` 目录权限
   - 确保有足够的磁盘空间

### 调试方法

运行测试脚本验证配置：
```cmd
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe test_server_gpt_image_1.py
```

## 性能特点

- **响应速度**: 通常比 DALL-E 模型更快
- **图像质量**: 高质量图像生成
- **资源使用**: 较低的网络带宽使用（无需下载 URL）
- **存储**: 直接保存到本地，无需临时下载

## 最佳实践

1. **提示词优化**: 使用详细、描述性的提示词
2. **尺寸选择**: 根据需求选择合适的图像尺寸
3. **批量生成**: 可以一次生成多张图像（最多 10 张）
4. **文件管理**: 定期清理 `images/` 目录中的旧文件

## 更新日志

### v1.1.0
- 添加 GPT-Image-1 模型支持
- 实现 base64 图像处理
- 更新工具描述和参数
- 添加专用启动脚本和配置文件
