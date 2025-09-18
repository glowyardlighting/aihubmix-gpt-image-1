# 安装指南

## 前置要求

在运行此 MCP 服务器之前，您需要安装 Python 3.7 或更高版本。

### Windows 安装 Python

1. **下载 Python**：
   - 访问 [Python 官网](https://www.python.org/downloads/)
   - 下载 Python 3.11 或更高版本（推荐）
   - 选择 "Windows installer (64-bit)"

2. **安装 Python**：
   - 运行下载的安装程序
   - ⚠️ **重要**：勾选 "Add Python to PATH" 选项
   - 选择 "Install Now" 或 "Customize installation"
   - 完成安装

3. **验证安装**：
   打开命令提示符（cmd）或 PowerShell，运行：
   ```cmd
   python --version
   ```
   应该显示类似 `Python 3.11.x` 的版本信息。

### 替代安装方法

#### 使用 Microsoft Store
1. 打开 Microsoft Store
2. 搜索 "Python"
3. 安装 "Python 3.11" 或最新版本

#### 使用 Chocolatey（如果已安装）
```powershell
choco install python
```

#### 使用 Scoop（如果已安装）
```powershell
scoop install python
```

## 安装项目依赖

安装 Python 后，在项目目录中运行：

```cmd
cd "C:\Users\admin\Desktop\aihubmix-image-mcp-server"
pip install -r requirements.txt
```

## 配置 API 密钥

您的 API 密钥已经配置在 `.env` 文件中：
- API 地址：https://aihubmix.com/v1
- API 密钥：sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2

## 测试服务器

安装完成后，运行测试：

```cmd
python test_server.py
```

## 启动服务器

```cmd
python server.py
```

或者双击 `start.bat` 文件。

## 在 Claude Code 中使用

1. 打开 Claude Code
2. 在设置中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "aihubmix-image": {
      "command": "python",
      "args": ["C:\\Users\\admin\\Desktop\\aihubmix-image-mcp-server\\server.py"],
      "env": {
        "AIHUBMIX_API_KEY": "sk-nX1g2sjjTRedR3RI77A3E3D9Dc8f4cEfB0A7144aDc4e6aA2"
      }
    }
  }
}
```

## 故障排除

### Python 未找到
- 确保 Python 已安装并添加到 PATH
- 重启命令提示符/PowerShell
- 尝试使用完整路径：`C:\Users\admin\AppData\Local\Programs\Python\Python311\python.exe`

### 依赖安装失败
- 确保网络连接正常
- 尝试使用国内镜像：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/`

### API 连接失败
- 检查 API 密钥是否正确
- 确认网络可以访问 https://aihubmix.com
- 检查账户余额是否充足