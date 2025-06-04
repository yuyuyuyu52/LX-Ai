#!/usr/bin/env python3
"""
验证码按钮功能最终测试脚本
测试验证码按钮的完整流程
"""

import requests
import json
import time
from urllib.parse import urljoin

# 测试配置
BASE_URL = "http://127.0.0.1:8001"
TEST_PHONE = "13800138000"

def test_verification_flow():
    """测试完整的验证码流程"""
    print("=== 验证码功能最终测试 ===")
    
    session = requests.Session()
    
    # 1. 获取注册页面和CSRF token
    print("\n1. 获取注册页面...")
    register_url = urljoin(BASE_URL, "/register/")
    response = session.get(register_url)
    
    if response.status_code != 200:
        print(f"❌ 注册页面访问失败: {response.status_code}")
        return False
    
    print(f"✅ 注册页面访问成功: {response.status_code}")
    
    # 提取CSRF token
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.text:
        import re
        match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if match:
            csrf_token = match.group(1)
            print(f"✅ CSRF token获取成功: {csrf_token[:20]}...")
        else:
            print("❌ CSRF token解析失败")
            return False
    else:
        print("❌ 页面中未找到CSRF token")
        return False
    
    # 2. 测试验证码发送
    print(f"\n2. 测试发送验证码到手机号: {TEST_PHONE}")
    send_code_url = urljoin(BASE_URL, "/get-code/")
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrf_token,
        'Referer': register_url,
    }
    
    data = {
        'phone': TEST_PHONE
    }
    
    response = session.post(send_code_url, headers=headers, data=data)
    
    print(f"发送验证码响应状态: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result.get('success'):
                print(f"✅ 验证码发送成功!")
                if 'code' in result:
                    print(f"📱 验证码: {result['code']}")
                return True
            else:
                print(f"❌ 验证码发送失败: {result.get('message', '未知错误')}")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ 响应JSON解析失败: {e}")
            print(f"原始响应内容: {response.text[:500]}")
            return False
    else:
        print(f"❌ 验证码发送请求失败: {response.status_code}")
        print(f"响应内容: {response.text[:500]}")
        return False

def test_button_click_simulation():
    """模拟浏览器中的按钮点击"""
    print("\n=== 模拟按钮点击测试 ===")
    
    # 测试页面内容检查
    session = requests.Session()
    register_url = urljoin(BASE_URL, "/register/")
    response = session.get(register_url)
    
    page_content = response.text
    
    # 检查关键元素是否存在
    checks = [
        ('sendVerificationBtn', 'id="sendVerificationBtn"' in page_content),
        ('手机号输入框', 'id="id_phone_number"' in page_content),
        ('验证码输入框', 'id="id_verification_code"' in page_content),
        ('获取验证码按钮文本', '获取验证码' in page_content),
        ('JavaScript脚本', 'sendVerificationCode' in page_content),
        ('CSRF token', 'csrfmiddlewaretoken' in page_content),
    ]
    
    print("页面元素检查:")
    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {'存在' if passed else '缺失'}")
        if not passed:
            all_passed = False
    
    return all_passed

def main():
    """主测试函数"""
    print("开始验证码按钮功能完整测试")
    print(f"测试目标: {BASE_URL}")
    print(f"测试手机号: {TEST_PHONE}")
    print("=" * 50)
    
    # 页面元素测试
    page_test = test_button_click_simulation()
    
    # 验证码流程测试
    flow_test = test_verification_flow()
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print(f"  页面元素检查: {'✅ 通过' if page_test else '❌ 失败'}")
    print(f"  验证码流程测试: {'✅ 通过' if flow_test else '❌ 失败'}")
    
    if page_test and flow_test:
        print("\n🎉 所有测试通过！验证码功能正常工作。")
        print("\n📝 测试建议:")
        print("1. 在浏览器中打开 http://127.0.0.1:8001/register/")
        print("2. 输入手机号 13800138000")
        print("3. 点击'获取验证码'按钮")
        print("4. 检查控制台日志和页面状态显示")
        print("5. 使用显示的测试验证码完成注册")
        return True
    else:
        print("\n❌ 部分测试失败，需要进一步检查。")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
