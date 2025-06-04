#!/usr/bin/env python3
"""
测试会员购买流程修复
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, '/Users/Zhuanz/Documents/LX-Ai')

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

import django
django.setup()

import requests
from django.test import Client
from django.contrib.auth.models import User

from core.models import MembershipPlan, MembershipOrder, UserProfile

def test_membership_purchase_flow():
    """测试会员购买流程"""
    print("🔍 开始测试会员购买流程...")
    
    # 创建测试客户端
    client = Client()
    
    # 创建测试用户
    try:
        user = User.objects.get(username='testuser')
        print(f"✅ 使用现有测试用户: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✅ 创建新测试用户: {user.username}")
    
    # 确保用户有profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        print("✅ 创建用户档案")
    
    # 登录用户
    login_success = client.login(username='testuser', password='testpass123')
    if login_success:
        print("✅ 用户登录成功")
    else:
        print("❌ 用户登录失败")
        return False
    
    # 获取会员套餐
    plans = MembershipPlan.objects.filter(is_active=True)
    if not plans.exists():
        print("❌ 没有可用的会员套餐")
        return False
    
    plan = plans.first()
    print(f"✅ 找到会员套餐: {plan.name} - {plan.price}元")
    
    # 测试购买页面访问
    try:
        response = client.get(f'/membership/purchase/{plan.id}/')
        if response.status_code == 200:
            print("✅ 购买页面访问成功")
        else:
            print(f"❌ 购买页面访问失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 购买页面访问异常: {e}")
        return False
    
    # 测试创建订单
    try:
        order_count_before = MembershipOrder.objects.count()
        
        # 提交购买表单
        response = client.post(f'/membership/purchase/{plan.id}/', {
            'plan_id': plan.id,
            'payment_method': 'mock'
        })
        
        if response.status_code == 302:  # 重定向到支付页面
            print("✅ 订单创建成功，重定向到支付页面")
            
            # 检查订单是否真的创建了
            order_count_after = MembershipOrder.objects.count()
            if order_count_after > order_count_before:
                print("✅ 订单已保存到数据库")
                
                # 获取最新创建的订单
                latest_order = MembershipOrder.objects.filter(user=user).latest('created_at')
                print(f"✅ 订单详情: {latest_order.order_id} - {latest_order.amount}元")
                
                # 测试支付页面
                payment_url = response.url
                print(f"✅ 支付页面URL: {payment_url}")
                
                # 访问支付页面
                payment_response = client.get(payment_url)
                if payment_response.status_code == 200:
                    print("✅ 支付页面访问成功")
                    
                    # 测试支付处理
                    process_response = client.post(f'/membership/process-payment/{latest_order.order_id}/', 
                        content_type='application/json',
                        data='{"order_id": "' + latest_order.order_id + '", "payment_method": "mock"}'
                    )
                    
                    if process_response.status_code == 200:
                        process_data = process_response.json()
                        if process_data.get('success'):
                            print("✅ 支付处理成功")
                            
                            # 检查订单状态是否更新
                            latest_order.refresh_from_db()
                            if latest_order.status == 'paid':
                                print("✅ 订单状态已更新为已支付")
                                
                                # 检查会员是否激活
                                profile.refresh_from_db()
                                if profile.is_vip():
                                    print("✅ 会员已成功激活")
                                    print(f"✅ 会员到期时间: {profile.membership_expire_date}")
                                    return True
                                else:
                                    print("❌ 会员未激活")
                            else:
                                print(f"❌ 订单状态未更新，当前状态: {latest_order.status}")
                        else:
                            print(f"❌ 支付处理失败: {process_data.get('message', '未知错误')}")
                    else:
                        print(f"❌ 支付处理请求失败，状态码: {process_response.status_code}")
                else:
                    print(f"❌ 支付页面访问失败，状态码: {payment_response.status_code}")
            else:
                print("❌ 订单未保存到数据库")
        else:
            print(f"❌ 订单创建失败，状态码: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"响应内容: {response.content.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ 订单创建异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

def test_url_patterns():
    """测试URL模式"""
    print("\n🔍 测试URL模式...")
    
    from django.urls import reverse
    
    try:
        # 测试会员相关URL
        urls_to_test = [
            ('core:membership_plans', {}),
            ('core:purchase_membership', {'plan_id': 1}),
            ('core:membership_payment', {'order_id': 'test123'}),
            ('core:process_payment', {'order_id': 'test123'}),
            ('core:membership_success', {}),
            ('core:membership_orders', {}),
            ('core:membership_status', {}),
        ]
        
        for url_name, kwargs in urls_to_test:
            try:
                url = reverse(url_name, kwargs=kwargs)
                print(f"✅ {url_name}: {url}")
            except Exception as e:
                print(f"❌ {url_name}: {e}")
                
    except Exception as e:
        print(f"❌ URL测试异常: {e}")

if __name__ == '__main__':
    print("🚀 开始测试会员系统修复...")
    
    # 测试URL模式
    test_url_patterns()
    
    # 测试购买流程
    success = test_membership_purchase_flow()
    
    if success:
        print("\n🎉 所有测试通过！会员购买流程修复成功！")
    else:
        print("\n❌ 测试失败，需要进一步检查")
    
    print("\n📊 系统状态总结:")
    print(f"- 会员套餐数量: {MembershipPlan.objects.count()}")
    print(f"- 订单总数: {MembershipOrder.objects.count()}")
    print(f"- 用户总数: {User.objects.count()}")
    print(f"- VIP用户数量: {UserProfile.objects.filter(membership='vip').count()}")
