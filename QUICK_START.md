# 快速开始指南

## 项目已配置完成！

您的 AIHubMix Image MCP Server 已经配置完成，可以直接使用。

### 当前配置
- **API 地址**: https://aihubmix.com/v1
- **API 密钥**: sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2
- **Python 路径**: C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe

## 启动服务器

### 方法 1: 使用启动脚本（推荐）
双击 `start.bat` 文件

### 方法 2: 命令行启动
```cmd
cd "C:\Users\admin\Desktop\aihubmix-image-mcp-server"
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe server.py
```

## 在 Claude Code 中使用

1. 打开 Claude Code
2. 在设置中找到 MCP 服务器配置
3. 添加以下配置：

```json
{
  "mcpServers": {
    "aihubmix-image": {
      "command": "C:\\Users\\admin\\AppData\\Local\\Programs\\Python\\Python38\\python.exe",
      "args": ["C:\\Users\\admin\\Desktop\\aihubmix-image-mcp-server\\server.py"],
      "env": {
        "AIHUBMIX_API_KEY": "sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2",
        "AIHUBMIX_BASE_URL": "https://aihubmix.com/v1"
      }
    }
  }
}
```

或者直接复制 `claude-code-config.json` 文件中的内容。

## 测试服务器

运行测试脚本验证配置：
```cmd
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe simple_test.py
```

## 使用示例

在 Claude Code 中，您可以这样使用：

```
生成一张宁静的山景日落图像，有水晶般清澈的湖泊，保存为 mountain_sunset.png
```

生成的图像将自动保存到 `images/` 文件夹中。

## 支持的功能

- **模型**: DALL-E 3, DALL-E 2
- **尺寸**: 1024x1024, 1792x1024, 1024x1792
- **质量**: standard, hd (仅 DALL-E 3)
- **风格**: vivid, natural (仅 DALL-E 3)
- **数量**: 1-4 张图像

## 故障排除

如果遇到问题，请运行：
```cmd
C:\Users\admin\AppData\Local\Programs\Python\Python38\python.exe simple_check.py
```

## 文件说明

- `server.py` - 主服务器文件
- `start.bat` - Windows 启动脚本
- `simple_test.py` - 测试脚本
- `simple_check.py` - 配置检查脚本
- `test_image_save.py` - 图片保存功能测试脚本
- `claude-code-config.json` - Claude Code 配置文件
- `.env` - 环境变量配置（已配置好）
- `images/` - 生成的图片保存文件夹

## 下一步

1. 启动服务器
2. 在 Claude Code 中配置 MCP 服务器
3. 开始生成图像！

祝您使用愉快！