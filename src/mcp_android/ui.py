"""
UI操作模块 - 提供Android UI自动化操作功能
"""

from typing import Optional
import time
from .android import get_device

def click_element(
    text: Optional[str] = None,
    description: Optional[str] = None,
    resourceId: Optional[str] = None,
    xpath: Optional[str] = None,
) -> bool:
    """
    点击界面元素
    Args:
        text: 通过文本内容定位
        description: 通过描述内容定位
        resourceId: 通过资源ID定位
        xpath: 通过xpath定位
    Returns:
        bool: 是否点击成功
    """
    device = get_device()
    selector = device.xpath
    
    if text:
        element = device(text=text)
    elif description:
        element = device(description=description)
    elif resourceId:
        element = device(resourceId=resourceId)
    elif xpath:
        element = selector(xpath)
    else:
        return False
        
    if element.exists:
        element.click()
        return True
    return False

def input_text(text: str, clear: bool = True) -> None:
    """
    在当前焦点输入框中输入文本
    Args:
        text: 要输入的文本
        clear: 是否在输入前清除现有内容
    """
    device = get_device()
    if clear:
        device.clear_text()
    device.send_keys(text)

def swipe_screen(direction: str, scale: float = 0.9) -> None:
    """
    滑动屏幕
    Args:
        direction: 滑动方向，支持 'up', 'down', 'left', 'right'
        scale: 滑动比例，默认0.9
    """
    device = get_device()
    window_size = device.window_size()
    width, height = window_size[0], window_size[1]
    
    start_x = width // 2
    start_y = height // 2
    
    if direction == "up":
        end_x = start_x
        end_y = int(start_y * (1 - scale))
    elif direction == "down":
        end_x = start_x
        end_y = int(start_y * (1 + scale))
    elif direction == "left":
        end_x = int(start_x * (1 - scale))
        end_y = start_y
    elif direction == "right":
        end_x = int(start_x * (1 + scale))
        end_y = start_y
    else:
        raise ValueError("Invalid direction. Must be one of: up, down, left, right")
        
    device.swipe(start_x, start_y, end_x, end_y)

def wait_and_click_element(
    text: Optional[str] = None,
    description: Optional[str] = None,
    timeout: int = 10
) -> bool:
    """
    等待元素出现并点击
    Args:
        text: 要等待的文本内容
        description: 要等待的描述内容
        timeout: 超时时间（秒）
    Returns:
        bool: 是否点击成功
    """
    device = get_device()
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if text and device(text=text).exists:
            return click_element(text=text)
        elif description and device(description=description).exists:
            return click_element(description=description)
        time.sleep(0.5)
    
    return False

def scroll_to_element(
    text: Optional[str] = None,
    description: Optional[str] = None
) -> bool:
    """
    滚动到指定元素
    Args:
        text: 要查找的文本
        description: 要查找的描述
    Returns:
        bool: 是否找到并滚动到元素
    """
    device = get_device()
    
    if text:
        return device(scrollable=True).scroll.to(text=text)
    elif description:
        return device(scrollable=True).scroll.to(description=description)
    return False 