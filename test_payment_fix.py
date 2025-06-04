#!/usr/bin/env python3
import os
import sys
import django
from pathlib import Path

# 设置Django项目路径
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import UserProfile, MembershipPlan, MembershipOrder
import json

def test_payment_flow():
    print('🔍 测试支付流程修复...')
    
    # 创建测试客户端
    client = Client()
    
    # 获取测试用户
    user = User.objects.filter(username='testuser').first()
    if not user:
        print('❌ 测试用户不存在')
        return False
    
    # 登录用户
    client.force_login(user)
    print('✅ 用户登录成功')
    
    # 获取会员套餐
    plan = MembershipPlan.objects.first()
    if not plan:
        print('❌ 没有可用的会员套餐')
        return False
    
    # 创建测试订单
    order = MembershipOrder.objects.create(
        user=user,
        plan=plan,
        amount=plan.price,
        payment_method='mock'
    )
    print(f'✅ 创建测试订单: {order.order_id}')
    
    # 测试支付页面访问
    payment_url = f'/membership/payment/{order.order_id}/'
    response = client.get(payment_url)
    print(f'✅ 支付页面访问状态: {response.status_code}')
    
    if response.status_code != 200:
        print(f'❌ 支付页面访问失败: {response.content}')
        return False
    
    # 检查页面内容是否包含CSRF令牌
    content = response.content.decode('utf-8')
    if 'csrfmiddlewaretoken' in content:
        print('✅ CSRF令牌已包含在页面中')
    else:
        print('❌ 页面中缺少CSRF令牌')
        return False
    
    # 测试支付处理
    process_url = f'/membership/process-payment/{order.order_id}/'
    
    # 获取CSRF令牌
    csrf_token = client.cookies['csrftoken'].value
    
    response = client.post(process_url, 
        data=json.dumps({
            'order_id': order.order_id,
            'payment_method': 'mock'
        }),
        content_type='application/json',
        HTTP_X_CSRFTOKEN=csrf_token
    )
    
    print(f'✅ 支付处理响应状态: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print('✅ 支付处理成功')
            
            # 检查订单状态
            order.refresh_from_db()
            if order.status == 'paid':
                print('✅ 订单状态已更新为已支付')
                
                # 检查用户会员状态
                user.userprofile.refresh_from_db()
                if user.userprofile.is_vip:
                    print('✅ 用户会员状态已激活')
                    return True
                else:
                    print('❌ 用户会员状态未激活')
            else:
                print(f'❌ 订单状态异常: {order.status}')
        else:
            print(f'❌ 支付处理失败: {data.get("message", "未知错误")}')
    else:
        print(f'❌ 支付请求失败: {response.content}')
    
    return False

if __name__ == '__main__':
    success = test_payment_flow()
    if success:
        print('\n🎉 支付流程修复成功！')
    else:
        print('\n⚠️ 支付流程仍有问题，需要进一步检查')
