"""
UIAutomator2 MCP Server - Android自动化测试MCP服务器
"""

from .android import (
    execute_adb_shell_command,
    get_packages,
    get_screenshot,
)
from .ui import (
    click_element,
    input_text,
    swipe_screen,
    wait_and_click_element,
    scroll_to_element,
)
from .app import (
    start_app,
    stop_app,
    get_current_app,
    init_uiautomator2,
    check_uiautomator2,
    restart_uiautomator2,
)

__version__ = "0.1.0"

__all__ = [
    "execute_adb_shell_command",
    "get_packages",
    "get_screenshot",
    "click_element",
    "input_text",
    "swipe_screen",
    "wait_and_click_element",
    "scroll_to_element",
    "start_app",
    "stop_app",
    "get_current_app",
    "init_uiautomator2",
    "check_uiautomator2",
    "restart_uiautomator2",
] 