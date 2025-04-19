"""
UIAutomator2 MCP Server - 服务器入口
"""

import logging
from fastmcp import FastMCP
from mcp_android import (
    execute_adb_shell_command,
    get_packages,
    get_screenshot,
    click_element,
    input_text,
    swipe_screen,
    wait_and_click_element,
    scroll_to_element,
    start_app,
    stop_app,
    get_current_app,
    init_uiautomator2,
    check_uiautomator2,
    restart_uiautomator2,
)
from mcp_android.ocr import ocr_manager
from typing import List, Dict, Optional, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/mcp-android.log')
    ]
)

# 创建MCP服务器实例
mcp = FastMCP("UIAutomator2 MCP Server")

# 初始化设备
try:
    init_result = init_uiautomator2()
    logging.info(f"Device initialization result: {init_result}")
except Exception as e:
    logging.error(f"Failed to initialize device: {e}")
    raise

# Android设备管理工具
@mcp.tool("ADB_shell")
def mcp_android_execute_adb_shell_command(command: str) -> str:
    """执行ADB shell命令"""
    try:
        return execute_adb_shell_command(command)
    except Exception as e:
        logging.error(f"Failed to execute ADB command: {e}")
        raise

@mcp.tool("get_packages")
def mcp_android_get_packages() -> str:
    """获取已安装的应用包列表"""
    return get_packages()

@mcp.tool("get_screenshot")
def mcp_android_get_screenshot() -> bytes:
    """获取屏幕截图"""
    return get_screenshot()

# UI操作工具
@mcp.tool("click_element")
def mcp_android_click_element(
    text: Optional[str] = None,
    description: Optional[str] = None,
    resourceId: Optional[str] = None,
    xpath: Optional[str] = None,
) -> bool:
    """点击界面元素"""
    return click_element(text, description, resourceId, xpath)

@mcp.tool("input_text")
def mcp_android_input_text(text: str, clear: bool = True) -> None:
    """输入文本"""
    input_text(text, clear)

@mcp.tool("swipe_screen")
def mcp_android_swipe_screen(direction: str, scale: float = 0.9) -> None:
    """滑动屏幕"""
    swipe_screen(direction, scale)

@mcp.tool("wait_and_click")
def mcp_android_wait_and_click_element(
    text: Optional[str] = None,
    description: Optional[str] = None,
    timeout: int = 10,
) -> bool:
    """等待元素出现并点击"""
    return wait_and_click_element(text, description, timeout)

@mcp.tool("scroll_to_element")
def mcp_android_scroll_to_element(
    text: Optional[str] = None,
    description: Optional[str] = None,
) -> bool:
    """滚动到指定元素"""
    return scroll_to_element(text, description)

# 应用管理工具
@mcp.tool("start_app")
def mcp_android_start_app(package_name: str) -> bool:
    """启动应用"""
    return start_app(package_name)

@mcp.tool("stop_app")
def mcp_android_stop_app(package_name: str) -> None:
    """停止应用"""
    stop_app(package_name)

@mcp.tool("get_current_app")
def mcp_android_get_current_app() -> tuple:
    """获取当前运行的应用信息"""
    return get_current_app()

@mcp.tool("UIAutomator2")
def mcp_android_init_uiautomator2() -> str:
    """初始化UIAutomator2"""
    return init_uiautomator2()

@mcp.tool("check_uiautomator2")
def mcp_android_check_uiautomator2() -> dict:
    """检查UIAutomator2状态"""
    return check_uiautomator2()

@mcp.tool("restart_uiautomator2")
def mcp_android_restart_uiautomator2() -> str:
    """重启UIAutomator2服务"""
    return restart_uiautomator2()

# OCR工具
@mcp.tool("OCR")
def mcp_android_ocr_screen() -> List[Dict]:
    """获取当前屏幕的OCR识别结果"""
    return ocr_manager.ocr_screen()

@mcp.tool("find_text")
def mcp_android_find_text_position(text: str, confidence_threshold: float = 0.5) -> Optional[Tuple[int, int]]:
    """查找文本位置"""
    return ocr_manager.find_text_position(text, confidence_threshold)

@mcp.tool("click_text")
def mcp_android_click_text(text: str, confidence_threshold: float = 0.5) -> bool:
    """点击指定文本"""
    return ocr_manager.click_text(text, confidence_threshold)

@mcp.tool("click_position")
def mcp_android_click_position(x: int, y: int) -> bool:
    """点击指定坐标"""
    return ocr_manager.click_position(x, y)

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise 