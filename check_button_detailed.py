#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def check_button_functionality():
    """检查按钮功能的详细状态"""
    print("🔍 检查验证码按钮详细状态...")
    print("=" * 60)
    
    try:
        # 获取注册页面
        response = requests.get('http://127.0.0.1:8003/register/')
        if response.status_code != 200:
            print(f"❌ 页面访问失败: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. 检查按钮元素
        print("1️⃣ 检查按钮元素...")
        btn = soup.find('button', {'id': 'sendVerificationBtn'})
        if btn:
            print(f"✅ 按钮找到: {btn}")
            print(f"   - type: {btn.get('type')}")
            print(f"   - class: {btn.get('class')}")
            print(f"   - id: {btn.get('id')}")
            print(f"   - 文本: {btn.get_text().strip()}")
        else:
            print("❌ 按钮未找到！")
            return
        
        # 2. 检查手机号输入框
        print("\n2️⃣ 检查手机号输入框...")
        phone_input = soup.find('input', {'id': 'id_phone_number'})
        if phone_input:
            print(f"✅ 手机号输入框找到: {phone_input}")
            print(f"   - name: {phone_input.get('name')}")
            print(f"   - id: {phone_input.get('id')}")
            print(f"   - class: {phone_input.get('class')}")
        else:
            print("❌ 手机号输入框未找到！")
        
        # 3. 检查JavaScript代码
        print("\n3️⃣ 检查JavaScript代码...")
        scripts = soup.find_all('script')
        js_content = ""
        for script in scripts:
            if script.string:
                js_content += script.string
        
        # 检查关键代码片段
        checks = [
            ("DOMContentLoaded", "页面加载事件"),
            ("sendVerificationBtn", "按钮变量"),
            ("addEventListener", "事件监听器"),
            ("click", "点击事件"),
            ("validatePhoneNumber", "手机号验证函数"),
            ("fetch('/get-code/'", "验证码请求"),
        ]
        
        for check, desc in checks:
            if check in js_content:
                print(f"✅ {desc}: 找到")
            else:
                print(f"❌ {desc}: 未找到")
        
        # 4. 检查可能的JavaScript错误源
        print("\n4️⃣ 检查可能的问题...")
        
        # 检查是否有其他同名元素
        all_buttons = soup.find_all('button')
        print(f"页面总共有 {len(all_buttons)} 个按钮")
        
        for i, button in enumerate(all_buttons):
            print(f"  按钮 {i+1}: id='{button.get('id')}', type='{button.get('type')}', text='{button.get_text().strip()}'")
        
        # 检查表单结构
        form = soup.find('form')
        if form:
            print(f"✅ 表单找到: method='{form.get('method')}', class='{form.get('class')}'")
        else:
            print("❌ 表单未找到")
        
        # 5. 检查CSS可能的干扰
        print("\n5️⃣ 检查CSS样式...")
        style_tags = soup.find_all('style')
        css_content = ""
        for style in style_tags:
            if style.string:
                css_content += style.string
        
        if 'btn-outline-zen' in css_content:
            print("✅ 按钮样式类存在")
        else:
            print("❌ 按钮样式类缺失")
        
        # 检查可能的覆盖样式
        if 'pointer-events: none' in css_content:
            print("⚠️ 发现 pointer-events: none，可能阻止点击")
        
        if 'disabled' in css_content:
            print("✅ 发现禁用状态样式")
        
        print("\n" + "=" * 60)
        print("🎯 问题诊断完成")
        
    except Exception as e:
        print(f"❌ 检查过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_button_functionality()
