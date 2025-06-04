#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time

def test_verification_button():
    """测试验证码按钮功能"""
    print("🔍 测试验证码按钮功能...")
    print("=" * 50)
    
    try:
        # 1. 访问注册页面
        print("1️⃣ 访问注册页面...")
        response = requests.get('http://127.0.0.1:8003/register/')
        if response.status_code != 200:
            print(f"❌ 注册页面访问失败，状态码: {response.status_code}")
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        print("✅ 注册页面访问成功")
        
        # 2. 检查验证码按钮是否存在
        verification_btn = soup.find('button', {'id': 'sendVerificationBtn'})
        if not verification_btn:
            print("❌ 找不到验证码按钮！")
            return False
        print("✅ 验证码按钮存在")
        
        # 3. 检查手机号输入框
        phone_input = soup.find('input', {'id': 'id_phone_number'})
        if not phone_input:
            print("❌ 找不到手机号输入框！")
            return False
        print("✅ 手机号输入框存在")
        
        # 4. 检查JavaScript代码
        script_tags = soup.find_all('script')
        js_code = ""
        for script in script_tags:
            if script.string:
                js_code += script.string
        
        # 检查关键JavaScript函数
        required_functions = [
            'sendVerificationBtn.addEventListener',
            'validatePhoneNumber',
            'showVerificationStatus',
            'startCountdown'
        ]
        
        missing_functions = []
        for func in required_functions:
            if func not in js_code:
                missing_functions.append(func)
        
        if missing_functions:
            print(f"❌ JavaScript中缺少关键函数: {missing_functions}")
            return False
        
        print("✅ JavaScript关键函数都存在")
        
        # 5. 检查CSS样式
        css_content = response.text
        required_styles = [
            'btn-outline-zen',
            'verification-status',
            'zen-form-control'
        ]
        
        missing_styles = []
        for style in required_styles:
            if style not in css_content:
                missing_styles.append(style)
        
        if missing_styles:
            print(f"❌ CSS中缺少关键样式: {missing_styles}")
            return False
        
        print("✅ CSS样式完整")
        
        # 6. 测试验证码发送接口
        print("\n2️⃣ 测试验证码发送接口...")
        csrf_token_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.text)
        if not csrf_token_match:
            print("❌ 找不到CSRF令牌")
            return False
        
        csrf_token = csrf_token_match.group(1)
        print("✅ CSRF令牌获取成功")
        
        # 发送验证码请求
        verification_data = {
            'phone': '13800138000'
        }
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://127.0.0.1:8003/register/'
        }
        
        # 先获取cookies
        session = requests.Session()
        session.get('http://127.0.0.1:8003/register/')
        
        verify_response = session.post(
            'http://127.0.0.1:8003/get-code/',
            data=verification_data,
            headers=headers
        )
        
        if verify_response.status_code == 200:
            result = verify_response.json()
            print(f"✅ 验证码接口响应: {result}")
            
            if result.get('success'):
                print("✅ 验证码发送功能正常")
                if result.get('code'):
                    print(f"📱 测试验证码: {result['code']}")
            else:
                print(f"⚠️ 验证码发送被限制: {result.get('message', '未知错误')}")
        else:
            print(f"❌ 验证码接口请求失败，状态码: {verify_response.status_code}")
            return False
        
        print("\n" + "=" * 50)
        print("✨ 验证码按钮功能测试完成")
        print("\n📋 诊断建议:")
        print("1. 如果按钮仍然无响应，请打开浏览器开发者工具")
        print("2. 查看Console选项卡是否有JavaScript错误")
        print("3. 确保手机号输入框有值且格式正确")
        print("4. 检查Network选项卡确认请求是否发送")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_verification_button()
