"""
专门测试 UIAutomator2 初始化功能
"""

from mcp_android import init_uiautomator2, check_uiautomator2, restart_uiautomator2

def test_init():
    """测试初始化过程"""
    print("\n=== 测试 UIAutomator2 初始化 ===")
    
    print("1. 直接调用初始化")
    try:
        result = init_uiautomator2()
        print(f"初始化结果: {result}")
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        print(f"错误类型: {type(e)}")
    
    print("\n2. 检查服务状态")
    try:
        status = check_uiautomator2()
        print(f"服务状态: {status}")
    except Exception as e:
        print(f"状态检查失败: {str(e)}")
        print(f"错误类型: {type(e)}")
    
    print("\n3. 尝试重启服务")
    try:
        restart_result = restart_uiautomator2()
        print(f"重启结果: {restart_result}")
    except Exception as e:
        print(f"重启失败: {str(e)}")
        print(f"错误类型: {type(e)}")

if __name__ == "__main__":
    test_init() 