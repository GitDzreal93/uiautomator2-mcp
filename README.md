# UIAutomator2 MCP Server

基于FastMCP框架实现的UIAutomator2 MCP服务器,提供Android设备自动化控制能力。

## 功能特性

- Android设备管理
  - ADB命令执行
  - 应用包管理
  - 屏幕截图

- UI自动化操作
  - 元素点击
  - 文本输入
  - 屏幕滑动
  - 元素等待
  - 页面滚动

- 应用管理
  - 应用启动/停止
  - 当前应用信息
  - UIAutomator2服务管理

## 环境要求

- Python 3.10+
- ADB工具
- Android设备或模拟器

## 安装

1. 克隆项目
```bash
git clone https://github.com/yourusername/uiautomator2-mcp.git
cd uiautomator2-mcp
```

2. 安装依赖
```bash
pip install -e .
```

## MCP配置

### 1. 配置mcp.json

在Claude Desktop的配置目录下创建或编辑`mcp.json`文件（通常在`~/.cursor/mcp.json`或`%APPDATA%\Cursor\mcp.json`）：

```json
{
  "mcpServers": {
    "android": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/uiautomator2-mcp",  // 替换为你的项目路径
        "run",
        "src/server.py"
      ]
    }
  }
}
```

配置说明：
- `android`: MCP服务器的唯一标识符
- `command`: 用于运行Python的命令（这里使用uv，也可以使用python）
- `args`: 命令行参数
  - `--directory`: 项目目录路径
  - `run`: uv的运行命令
  - `src/server.py`: 服务器入口文件路径

### 2. 配置选项

你可以根据需要调整以下配置：

1. 使用Python直接运行：
```json
{
  "mcpServers": {
    "android": {
      "command": "python",
      "args": [
        "/path/to/uiautomator2-mcp/src/server.py"
      ]
    }
  }
}
```

2. 使用虚拟环境：
```json
{
  "mcpServers": {
    "android": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/path/to/uiautomator2-mcp/src/server.py"
      ]
    }
  }
}
```

3. 添加环境变量：
```json
{
  "mcpServers": {
    "android": {
      "command": "python",
      "args": [
        "/path/to/uiautomator2-mcp/src/server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/uiautomator2-mcp",
        "ANDROID_HOME": "/path/to/android-sdk"
      }
    }
  }
}
```

### 3. 多服务器配置

你可以在同一配置文件中定义多个MCP服务器：

```json
{
  "mcpServers": {
    "android": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/uiautomator2-mcp",
        "run",
        "src/server.py"
      ]
    },
    "android-debug": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/uiautomator2-mcp",
        "run",
        "src/server.py",
        "--debug"
      ]
    }
  }
}
```

## 使用工具

配置完成后，你可以在Claude中直接使用所有可用的工具：

```python
# 初始化UIAutomator2
await mcp.call_tool("mcp_android_init_uiautomator2", {})

# 启动应用
await mcp.call_tool("mcp_android_start_app", {
    "package_name": "com.example.app"
})

# 点击元素
await mcp.call_tool("mcp_android_click_element", {
    "text": "登录"
})
```

## 开发

1. 安装开发依赖
```bash
pip install -e ".[dev]"
```

2. 运行测试
```bash
pytest
```

## 贡献

欢迎提交Issue和Pull Request。

## 许可证

MIT License