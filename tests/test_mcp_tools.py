"""
手动测试 MCP 工具的测试脚本
"""

import time
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

def test_device_initialization():
    """测试设备初始化相关功能"""
    print("\n=== 测试设备初始化 ===")
    
    print("1. 初始化 UIAutomator2")
    try:
        result = init_uiautomator2()
        print(f"初始化结果: {result}")
        assert "successfully" in result, "初始化失败"
    except Exception as e:
        print(f"初始化失败: {e}")
        raise
    
    print("\n2. 检查 UIAutomator2 状态")
    try:
        status = check_uiautomator2()
        print(f"服务状态: {status}")
        assert status["service_running"], "服务未运行"
        assert status["app_installed"], "应用未安装"
    except Exception as e:
        print(f"检查状态失败: {e}")
        raise

def test_basic_device_info():
    """测试基本设备信息获取"""
    print("\n=== 测试基本设备信息 ===")
    
    print("1. 获取已安装应用列表")
    try:
        packages = get_packages()
        print(f"已安装应用列表: {packages[:200]}...")  # 只显示前200个字符
        assert "com.android" in packages, "无法获取系统应用"
    except Exception as e:
        print(f"获取应用列表失败: {e}")
        raise
    
    print("\n2. 获取当前运行的应用")
    try:
        package_name, activity_name = get_current_app()
        print(f"当前运行的应用: {package_name}")
        print(f"当前活动: {activity_name}")
        assert package_name, "无法获取当前应用包名"
    except Exception as e:
        print(f"获取当前应用失败: {e}")
        raise

def test_app_operations():
    """测试应用操作"""
    print("\n=== 测试应用操作 ===")
    
    # 获取已安装的应用列表
    packages = get_packages()
    
    # 尝试常见的系统应用
    TEST_APPS = [
        "com.android.settings",
        "com.android.chrome",
        "com.android.browser",
        "com.android.calculator2",
        "com.android.deskclock",
        "com.android.calendar"
    ]
    
    TEST_APP = None
    for app in TEST_APPS:
        if f"package:{app}" in packages:
            TEST_APP = app
            break
            
    if not TEST_APP:
        print("未找到合适的测试应用，跳过应用操作测试")
        return
        
    print(f"使用 {TEST_APP} 进行测试")
    
    # 首先停止当前运行的应用
    current_app = get_current_app()[0]
    if current_app and current_app != "com.android.launcher":
        try:
            stop_app(current_app)
            time.sleep(2)  # 等待应用停止
        except:
            pass
    
    print(f"1. 启动应用: {TEST_APP}")
    try:
        result = start_app(TEST_APP)
        print(f"启动结果: {result}")
        assert result, "应用启动失败"
        time.sleep(3)  # 增加等待时间
        
        # 验证应用是否成功启动
        current_app = get_current_app()[0]
        assert current_app == TEST_APP, f"应用未成功启动，当前应用: {current_app}"
    except Exception as e:
        print(f"启动应用失败: {e}")
        raise
    
    print(f"\n2. 停止应用: {TEST_APP}")
    try:
        result = stop_app(TEST_APP)
        print(f"停止结果: {result}")
        time.sleep(2)  # 增加等待时间
        
        # 验证应用是否成功停止
        current_app = get_current_app()[0]
        assert current_app != TEST_APP, "应用未成功停止"
        print("应用已停止")
    except Exception as e:
        print(f"停止应用失败: {e}")
        raise

def test_ui_operations():
    """测试UI操作"""
    print("\n=== 测试UI操作 ===")
    
    # 首先启动设置应用
    start_app("com.android.settings")
    time.sleep(2)
    
    print("1. 点击元素测试")
    try:
        # 尝试点击"网络和互联网"或"WLAN"（不同系统可能名称不同）
        result = click_element(text="网络和互联网") or click_element(text="WLAN")
        print(f"点击结果: {result}")
        assert result, "点击元素失败"
        time.sleep(1)
    except Exception as e:
        print(f"点击元素失败: {e}")
        raise
    
    print("\n2. 滑动屏幕测试")
    try:
        swipe_screen("up")
        time.sleep(1)
        swipe_screen("down")
        print("屏幕滑动完成")
    except Exception as e:
        print(f"滑动屏幕失败: {e}")
        raise

def test_advanced_ui_operations():
    """测试高级UI操作"""
    print("\n=== 测试高级UI操作 ===")
    
    print("1. 等待并点击元素")
    try:
        result = wait_and_click_element(text="关于手机", timeout=5)
        print(f"等待点击结果: {result}")
        time.sleep(1)
    except Exception as e:
        print(f"等待点击失败: {e}")
        raise
    
    print("\n2. 滚动到指定元素")
    try:
        result = scroll_to_element(text="监管标签")  # 通常在关于手机页面底部
        print(f"滚动结果: {result}")
        time.sleep(1)
    except Exception as e:
        print(f"滚动到元素失败: {e}")
        raise

def test_adb_commands():
    """测试ADB命令执行"""
    print("\n=== 测试ADB命令 ===")
    
    print("1. 执行基本ADB命令")
    try:
        result = execute_adb_shell_command("dumpsys window | grep mCurrentFocus")
        print(f"命令执行结果: {result}")
        assert result, "ADB命令执行失败"
    except Exception as e:
        print(f"ADB命令执行失败: {e}")
        raise

def main():
    """主测试流程"""
    print("开始MCP工具测试...\n")
    
    try:
        # 1. 首先测试设备初始化
        test_device_initialization()
        
        # 2. 测试基本设备信息
        test_basic_device_info()
        
        # 3. 测试应用操作
        test_app_operations()
        
        # 4. 测试UI操作
        test_ui_operations()
        
        # 5. 测试高级UI操作
        test_advanced_ui_operations()
        
        # 6. 测试ADB命令
        test_adb_commands()
        
        print("\n所有测试完成!")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        raise
    finally:
        # 清理：停止设置应用
        try:
            stop_app("com.android.settings")
        except:
            pass

if __name__ == "__main__":
    main() 