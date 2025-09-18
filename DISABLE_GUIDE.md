# 禁用 DALL-E 2 和 DALL-E 3 功能指南

## 概述

AIHubMix Image MCP Server 现在支持通过环境变量来禁用 DALL-E 2 和 DALL-E 3 图像生成功能。

## 禁用方法

### 方法 1: 环境变量（推荐）

在启动服务器前设置环境变量：

```bash
set ENABLE_IMAGE_GENERATION=false
```

### 方法 2: 使用禁用配置启动脚本

直接运行 `start_disabled.bat` 文件：

```cmd
start_disabled.bat
```

### 方法 3: 手动设置所有环境变量

```cmd
set AIHUBMIX_API_KEY=sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
set AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
set AIHUBMIX_MODEL=dall-e-3
set MCP_SERVER_NAME=aihubmix-image-mcp-server
set ENABLE_IMAGE_GENERATION=false
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe server.py
```

## 禁用后的行为

当图像生成功能被禁用时：

1. **工具列表**: 只提供 `get_server_status` 工具，不再提供 `generate_image` 工具
2. **图像生成请求**: 任何尝试调用 `generate_image` 的请求都会被拒绝，并返回错误信息
3. **服务器状态**: 可以通过 `get_server_status` 工具查看当前配置状态

## 验证禁用状态

运行测试脚本验证功能是否已正确禁用：

```cmd
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe test_disabled.py
```

## 重新启用

要重新启用图像生成功能，设置：

```bash
set ENABLE_IMAGE_GENERATION=true
```

或者直接运行原始的 `start.bat` 文件。

## 配置文件

- `config_disabled.env`: 禁用配置示例
- `start_disabled.bat`: 禁用模式启动脚本
- `test_disabled.py`: 功能禁用测试脚本

## 安全说明

禁用图像生成功能后：
- 服务器仍然可以启动和运行
- API 密钥仍然需要配置（用于服务器验证）
- 不会进行任何图像生成 API 调用
- 不会产生任何费用

## 使用场景

禁用功能适用于以下场景：
- 临时禁用图像生成功能
- 节省 API 调用费用
- 仅使用服务器状态查询功能
- 测试和开发环境
