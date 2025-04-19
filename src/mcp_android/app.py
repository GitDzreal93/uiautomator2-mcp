"""
应用管理模块 - 提供Android应用管理功能
"""

import uiautomator2 as u2
from typing import Tuple
import time
import subprocess
import os
from .android import _device, set_device, get_device

def init_uiautomator2() -> str:
    """
    初始化 uiautomator2，包括安装和启动服务
    Returns:
        str: 初始化结果信息
    """
    try:
        # 检查ADB服务是否运行
        try:
            subprocess.run(['adb', 'devices'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            return "Failed to initialize UIAutomator2: ADB service is not running"
        except FileNotFoundError:
            return "Failed to initialize UIAutomator2: ADB command not found"
            
        # 获取设备列表
        devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True).stdout
        if 'device' not in devices:
            return "Failed to initialize UIAutomator2: No device connected"
        
        # 初始化设备连接
        device = u2.connect()
        
        # 确保设备已连接
        if not device:
            return "Failed to initialize UIAutomator2: Could not establish connection"
            
        # 设置全局设备对象
        set_device(device)
            
        # 安装必要的APK
        try:
            device.app_install("https://github.com/openatx/android-uiautomator-server/releases/download/2.3.1/app-uiautomator.apk")
            device.app_install("https://github.com/openatx/android-uiautomator-server/releases/download/2.3.1/app-uiautomator-test.apk")
        except:
            pass  # 如果已经安装则忽略错误
            
        # 启动UIAutomator服务
        device.app_start("com.github.uiautomator")
        device.app_start("com.github.uiautomator.test")
        time.sleep(2)
        
        # 检查服务是否正常运行
        try:
            device.info
            return "UIAutomator2 initialized successfully"
        except:
            return "Failed to initialize UIAutomator2: Service not running after installation"
            
    except Exception as e:
        return f"Failed to initialize UIAutomator2: {str(e)}"

def check_uiautomator2() -> dict:
    """
    检查 uiautomator2 是否正确安装和运行
    Returns:
        dict: 包含检查结果的字典
    """
    global _device
    status = {
        "adb_server": False,
        "device_connected": False,
        "service_running": False,
        "app_installed": False,
        "device_info": None,
        "error": None
    }
    
    try:
        # 检查ADB服务
        try:
            subprocess.run(['adb', 'devices'], check=True, capture_output=True)
            status["adb_server"] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            status["error"] = "ADB server not running or not found"
            return status
            
        # 检查设备连接
        if _device is None:
            try:
                _device = u2.connect()
            except Exception as e:
                status["error"] = f"Failed to connect device: {str(e)}"
                return status
                
        status["device_connected"] = _device is not None
        
        if not status["device_connected"]:
            status["error"] = "No device connected"
            return status
            
        # 检查服务状态
        try:
            _device.info
            status["service_running"] = True
        except:
            status["service_running"] = False
        
        # 检查应用是否安装
        packages = _device.shell(['pm', 'list', 'packages']).output
        status["app_installed"] = "com.github.uiautomator" in packages
        
        # 获取设备信息
        try:
            status["device_info"] = {
                "serial": _device.serial,
                "info": _device.info
            }
        except:
            status["device_info"] = "Failed to get device info"
            
        return status
    except Exception as e:
        status["error"] = str(e)
        return status

def restart_uiautomator2() -> str:
    """
    重启 uiautomator2 服务
    Returns:
        str: 重启结果信息
    """
    global _device
    try:
        if _device is None:
            return "Device not initialized. Please call init_uiautomator2() first"
            
        # 停止现有服务
        _device.app_stop("com.github.uiautomator")
        _device.app_stop("com.github.uiautomator.test")
        time.sleep(1)
        
        # 强制停止uiautomator应用
        _device.shell('am force-stop com.github.uiautomator')
        _device.shell('am force-stop com.github.uiautomator.test')
        time.sleep(1)
        
        # 重新启动服务
        _device.app_start("com.github.uiautomator")
        _device.app_start("com.github.uiautomator.test")
        time.sleep(2)
        
        # 验证服务是否正常运行
        try:
            _device.info
            return "UIAutomator2 service restarted successfully"
        except:
            return "Failed to restart UIAutomator2: Service not running after restart"
                
    except Exception as e:
        return f"Failed to restart UIAutomator2 service: {str(e)}"

def start_app(package_name: str) -> bool:
    """
    启动应用
    Args:
        package_name: 应用包名
    Returns:
        bool: 是否启动成功
    """
    try:
        device = get_device()
        
        # 先停止应用，确保重新启动
        try:
            device.app_stop(package_name)
        except:
            pass
            
        # 启动应用
        device.app_start(package_name, wait=True)
        return True
    except Exception:
        return False

def stop_app(package_name: str) -> bool:
    """
    停止应用
    Args:
        package_name: 应用包名
    Returns:
        bool: 是否停止成功
    """
    try:
        device = get_device()
        device.app_stop(package_name)
        return True
    except Exception:
        return False

def get_current_app() -> Tuple[str, str]:
    """
    获取当前运行的应用包名和活动名
    Returns:
        Tuple[str, str]: (package_name, activity_name)
    """
    device = get_device()
    try:
        current = device.app_current()
        return current["package"], current["activity"]
    except Exception:
        return "", "" 