#!/usr/bin/env python
"""
测试会员系统部署状态
用于验证服务器部署后的会员功能
"""
import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import MembershipPlan, MembershipOrder, UserProfile

def test_membership_system():
    """测试会员系统完整性"""
    print("=" * 50)
    print("会员系统部署测试")
    print("=" * 50)
    
    # 1. 检查会员套餐
    print("\n1. 检查会员套餐数据:")
    plans = MembershipPlan.objects.filter(is_active=True)
    print(f"   活跃套餐数量: {plans.count()}")
    for plan in plans:
        print(f"   - {plan.name}: ¥{plan.price} ({plan.duration_days}天)")
    
    # 2. 检查URL路由
    print("\n2. 测试URL路由:")
    client = Client()
    
    # 测试会员页面
    response = client.get('/membership/')
    print(f"   会员套餐页面: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
    
    # 3. 检查模板文件
    print("\n3. 检查关键模板文件:")
    template_files = [
        'templates/core/membership_plans.html',
        'templates/core/purchase_membership.html', 
        'templates/core/membership_payment.html',
        'templates/core/membership_status.html',
        'templates/core/membership_orders.html'
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"   {template_file}: ✓")
        else:
            print(f"   {template_file}: ✗ (缺失)")
    
    # 4. 检查视图函数
    print("\n4. 检查视图函数:")
    try:
        from core import membership_views
        view_functions = [
            'membership_plans',
            'purchase_membership', 
            'membership_payment',
            'process_payment',
            'membership_status',
            'membership_orders'
        ]
        
        for func_name in view_functions:
            if hasattr(membership_views, func_name):
                print(f"   {func_name}: ✓")
            else:
                print(f"   {func_name}: ✗ (缺失)")
    except ImportError as e:
        print(f"   视图模块导入失败: {e}")
    
    # 5. 创建测试用户并测试购买流程
    print("\n5. 测试用户购买流程:")
    try:
        # 创建或获取测试用户
        test_user, created = User.objects.get_or_create(
            username='test_deployment_user',
            defaults={
                'email': 'test@example.com',
                'first_name': '测试',
                'last_name': '用户'
            }
        )
        
        # 创建用户档案
        profile, created = UserProfile.objects.get_or_create(
            user=test_user,
            defaults={'phone': '13800000000'}
        )
        
        print(f"   测试用户创建: ✓ (ID: {test_user.id})")
        
        # 登录测试
        client.force_login(test_user)
        response = client.get('/membership/')
        print(f"   登录后访问会员页面: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
        
        # 测试购买页面
        daily_plan = plans.filter(plan_type='daily').first()
        if daily_plan:
            response = client.get(f'/membership/purchase/{daily_plan.id}/')
            print(f"   访问购买页面: {response.status_code} {'✓' if response.status_code == 200 else '✗'}")
        
        print(f"   会员状态: {'VIP' if profile.is_vip else '普通用户'}")
        if profile.membership_expire_date:
            print(f"   会员到期时间: {profile.membership_expire_date}")
        
    except Exception as e:
        print(f"   用户测试失败: {e}")
    
    # 6. 数据库完整性检查
    print("\n6. 数据库完整性检查:")
    try:
        # 检查订单表
        order_count = MembershipOrder.objects.count()
        print(f"   会员订单总数: {order_count}")
        
        # 检查用户档案
        profile_count = UserProfile.objects.count()
        print(f"   用户档案总数: {profile_count}")
        
        vip_count = UserProfile.objects.filter(is_vip=True).count()
        print(f"   当前VIP用户数: {vip_count}")
        
    except Exception as e:
        print(f"   数据库检查失败: {e}")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

def test_specific_issue():
    """测试特定问题：服务器上缺少购买选项"""
    print("\n" + "=" * 50)
    print("特定问题诊断：服务器购买选项缺失")
    print("=" * 50)
    
    # 检查可能的原因
    print("\n检查可能原因:")
    
    # 1. 检查套餐是否激活
    active_plans = MembershipPlan.objects.filter(is_active=True)
    print(f"1. 激活的套餐数量: {active_plans.count()}")
    if active_plans.count() == 0:
        print("   ⚠️  没有激活的套餐！")
    
    # 2. 检查模板渲染
    client = Client()
    response = client.get('/membership/')
    
    if response.status_code == 200:
        content = response.content.decode()
        if '立即开通' in content or '购买' in content:
            print("2. 模板包含购买按钮: ✓")
        else:
            print("2. 模板缺少购买按钮: ✗")
        
        if 'membership_plans.html' in str(response.templates):
            print("3. 使用正确模板: ✓")
        else:
            print("3. 模板路径问题: ✗")
    else:
        print(f"2. 页面访问失败: {response.status_code}")
    
    # 3. 检查静态文件
    print("4. 检查关键静态文件:")
    static_files = [
        'static/css/zen.css',
        'static/js/membership.js'
    ]
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"   {file_path}: ✓")
        else:
            print(f"   {file_path}: ✗ (可能影响样式)")
    
    print("\n解决建议:")
    print("1. 检查服务器上的 DEBUG 设置")
    print("2. 确认数据库迁移已正确应用")
    print("3. 检查静态文件是否正确收集")
    print("4. 验证模板文件是否完整上传")

if __name__ == '__main__':
    test_membership_system()
    test_specific_issue()
