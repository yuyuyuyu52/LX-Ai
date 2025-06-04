"""
会员系统完整流程测试
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:8000'

def test_membership_flow():
    """测试完整的会员购买流程"""
    print("=== 会员系统完整流程测试 ===\n")
    
    session = requests.Session()
    
    # 1. 访问会员套餐页面
    print("1. 访问会员套餐页面...")
    response = session.get(f'{BASE_URL}/membership/')
    if response.status_code == 200:
        print("   ✓ 会员套餐页面访问成功")
        if '单日会员' in response.text:
            print("   ✓ 套餐信息显示正常")
        else:
            print("   ✗ 套餐信息显示异常")
    else:
        print(f"   ✗ 访问失败，状态码: {response.status_code}")
        return
    
    # 2. 检查会员状态API
    print("\n2. 测试会员状态API...")
    response = session.get(f'{BASE_URL}/api/membership/status/')
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✓ API访问成功")
            print(f"   VIP状态: {data.get('is_vip', False)}")
            print(f"   到期时间: {data.get('expires_at', '无')}")
        except json.JSONDecodeError:
            print("   ✗ API响应格式错误")
    else:
        print(f"   ✗ API访问失败，状态码: {response.status_code}")
    
    # 3. 测试购买流程（需要登录）
    print("\n3. 测试购买流程...")
    print("   注意: 购买流程需要用户登录，当前为匿名访问测试")
    
    # 访问购买页面（应该重定向到登录）
    response = session.post(f'{BASE_URL}/membership/purchase/1/', data={
        'plan': 1,
        'payment_method': 'alipay'
    }, allow_redirects=False)
    
    if response.status_code == 302:
        print("   ✓ 未登录用户正确重定向到登录页面")
    else:
        print(f"   ? 响应状态: {response.status_code}")
    
    # 4. 测试静态资源
    print("\n4. 测试静态资源...")
    css_response = session.get(f'{BASE_URL}/static/css/membership.css')
    if css_response.status_code == 200:
        print("   ✓ 会员样式文件加载成功")
    else:
        print(f"   ✗ 样式文件加载失败: {css_response.status_code}")
    
    print("\n=== 流程测试完成 ===")

def check_system_health():
    """检查系统健康状态"""
    print("\n=== 系统健康检查 ===")
    
    endpoints = [
        ('/', '首页'),
        ('/membership/', '会员套餐'),
        ('/api/membership/status/', '会员状态API'),
        ('/admin/', '管理后台'),
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', timeout=5)
            status = "✓" if response.status_code in [200, 302] else "✗"
            print(f"   {status} {name}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ✗ {name}: 连接失败 - {e}")
    
    print("\n=== 健康检查完成 ===")

if __name__ == '__main__':
    try:
        test_membership_flow()
        check_system_health()
    except requests.exceptions.ConnectionError:
        print("无法连接到Django服务器，请确保服务器正在运行：")
        print("python manage.py runserver 8000")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
