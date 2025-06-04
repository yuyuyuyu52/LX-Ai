"""
会员系统基础功能测试
"""
import os
import sys
import django

# 添加项目路径
sys.path.append('/Users/Zhuanz/Documents/LX-Ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from core.models import UserProfile, MembershipPlan, MembershipOrder, PaymentRecord

def test_membership_system():
    """测试会员系统基础功能"""
    print("=== 会员系统功能测试 ===\n")
    
    # 1. 测试会员套餐
    print("1. 检查会员套餐...")
    plans = MembershipPlan.objects.filter(is_active=True)
    print(f"   活跃套餐数量: {plans.count()}")
    for plan in plans:
        print(f"   - {plan.name}: ¥{plan.price}, {plan.duration_days}天")
    
    # 2. 创建测试用户
    print("\n2. 创建测试用户...")
    test_user, created = User.objects.get_or_create(
        username='test_vip_user',
        defaults={
            'email': 'test@example.com',
            'first_name': '测试',
            'last_name': '用户'
        }
    )
    
    profile, created = UserProfile.objects.get_or_create(
        user=test_user,
        defaults={
            'phone_number': '13800138000',
            'gender': '男'
        }
    )
    print(f"   用户创建状态: {'新建' if created else '已存在'}")
    print(f"   当前VIP状态: {'是' if profile.is_vip() else '否'}")
    
    # 3. 测试订单创建
    print("\n3. 测试订单创建...")
    daily_plan = MembershipPlan.objects.filter(plan_type='daily', is_active=True).first()
    if daily_plan:
        order = MembershipOrder.objects.create(
            user=test_user,
            plan=daily_plan,
            amount=daily_plan.price,
            status='paid',  # 直接设置为已支付进行测试
            payment_method='mock'
        )
        print(f"   订单号: {order.order_id}")
        print(f"   订单金额: ¥{order.amount}")
        print(f"   订单状态: {order.get_status_display()}")
        
        # 4. 测试会员激活
        print("\n4. 测试会员激活...")
        success = order.activate_membership()
        if success:
            profile.refresh_from_db()
            print(f"   激活成功: 是")
            print(f"   VIP状态: {'是' if profile.is_vip() else '否'}")
            if profile.membership_expire_date:
                print(f"   到期时间: {profile.membership_expire_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   激活失败")
        
        # 5. 测试支付记录
        print("\n5. 创建支付记录...")
        payment = PaymentRecord.objects.create(
            order=order,
            payment_method='mock',
            amount=order.amount,
            trade_no=f'MOCK_{order.order_id}',
            payment_data={'test': True}
        )
        print(f"   支付记录ID: {payment.id}")
        print(f"   交易号: {payment.trade_no}")
        
    else:
        print("   没有找到活跃的每日会员套餐")
    
    # 6. 统计信息
    print("\n6. 系统统计...")
    total_orders = MembershipOrder.objects.count()
    active_vips = UserProfile.objects.filter(
        membership='vip',
        membership_expire_date__gt=timezone.now()
    ).count()
    total_payments = PaymentRecord.objects.count()
    
    print(f"   总订单数: {total_orders}")
    print(f"   活跃VIP用户数: {active_vips}")
    print(f"   支付记录数: {total_payments}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_membership_system()
