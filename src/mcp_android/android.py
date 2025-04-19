"""
Android设备管理模块 - 提供基础的Android设备操作功能
"""

import uiautomator2 as u2
from typing import Optional, List
from PIL import Image
import io

# 全局设备对象
_device: Optional[u2.Device] = None

def set_device(device: u2.Device) -> None:
    """
    设置全局设备对象
    Args:
        device: UIAutomator2设备对象
    """
    global _device
    _device = device

def get_device() -> u2.Device:
    """
    获取当前设备对象,如果未初始化则抛出异常
    Returns:
        u2.Device: UIAutomator2设备对象
    Raises:
        RuntimeError: 设备未初始化时抛出
    """
    global _device
    if _device is None:
        raise RuntimeError("Device not initialized. Please call init_uiautomator2() first.")
    return _device

def execute_adb_shell_command(command: str) -> str:
    """
    执行ADB shell命令
    Args:
        command (str): 要执行的ADB shell命令
    Returns:
        str: 命令执行输出
    """
    device = get_device()
    result = device.shell(command)
    return result.output if hasattr(result, 'output') else str(result)

def get_packages() -> str:
    """
    获取所有已安装包
    Returns:
        str: 已安装包列表
    """
    device = get_device()
    result = device.shell(['pm', 'list', 'packages'])
    return result.output if hasattr(result, 'output') else str(result)

def get_screenshot() -> Image.Image:
    """
    获取屏幕截图
    Returns:
        Image: 截图对象
    """
    device = get_device()
    screenshot_data = device.screenshot(format='raw')
    if isinstance(screenshot_data, Image.Image):
        return screenshot_data
    elif isinstance(screenshot_data, bytes):
        return Image.open(io.BytesIO(screenshot_data))
    else:
        raise TypeError(f"Unexpected screenshot data type: {type(screenshot_data)}") 