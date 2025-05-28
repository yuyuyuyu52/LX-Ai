#!/usr/bin/env python
"""
灵汐命理平台功能测试脚本
静心测试，确保系统运行如意
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fatemaster.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, DivinationRecord, Notification
from datetime import datetime, timedelta

def test_models():
    """测试模型功能"""
    print("🧪 静心测试模型功能...")
    
    # 测试用户创建
    test_user, created = User.objects.get_or_create(
        username='lingxi_test_user',
        defaults={
            'email': 'test@lingxi.com',
            'first_name': '灵汐',
            'last_name': '测试用户'
        }
    )
      if created:
        print(f"✅ 创建灵汐测试用户: {test_user.username}")
    else:
        print(f"ℹ️ 灵汐测试用户已存在: {test_user.username}")
    
    # 测试用户档案
    profile, created = UserProfile.objects.get_or_create(
        user=test_user,
        defaults={
            'birth_date': datetime(1990, 5, 15, 10, 30),
            'birth_place': '江南水乡',
            'gender': 'male'
        }
    )
    
    if created:
        print(f"✅ 创建禅意用户档案: {profile}")
    else:
        print(f"ℹ️ 禅意用户档案已存在: {profile}")
    
    # 测试占卜记录
    divination, created = DivinationRecord.objects.get_or_create(
        user=test_user,
        divination_type='bazi',
        defaults={
            'question': '静心观命，求问人生方向',
            'result': '天地人和，命运自在心中。静心修身，自有贵人相助。'
        }
    )
    
    if created:
        print(f"✅ 创建占卜记录: {divination}")
    else:
        print(f"ℹ️ 占卜记录已存在: {divination}")
    
    # 测试通知
    notification, created = Notification.objects.get_or_create(
        user=test_user,
        title='测试通知',
        defaults={
            'message': '这是一个测试通知',
            'notification_type': 'info'
        }
    )
    
    if created:
        print(f"✅ 创建通知: {notification}")
    else:
        print(f"ℹ️ 通知已存在: {notification}")

def test_statistics():
    """测试统计功能"""
    print("\n📊 系统统计信息:")
    
    total_users = User.objects.count()
    total_divinations = DivinationRecord.objects.count()
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    
    print(f"👥 总用户数: {total_users}")
    print(f"🔮 总占卜次数: {total_divinations}")
    print(f"🔔 总通知数: {total_notifications}")
    print(f"📬 未读通知: {unread_notifications}")
    
    # 占卜类型统计
    print("\n🎯 占卜类型分布:")
    from django.db.models import Count
    divination_stats = DivinationRecord.objects.values('divination_type').annotate(
        count=Count('divination_type')
    ).order_by('-count')
    
    for stat in divination_stats:
        type_names = {
            'bazi': '八字分析',
            'tarot': '塔罗占卜',
            'meihua': '梅花易数',
            'yijing': '易经卜卦'
        }
        type_name = type_names.get(stat['divination_type'], stat['divination_type'])
        print(f"  - {type_name}: {stat['count']} 次")

def test_recent_activity():
    """测试最近活动"""
    print("\n📅 最近活动:")
    
    # 最近的占卜记录
    recent_divinations = DivinationRecord.objects.order_by('-created_at')[:5]
    print("🔮 最近占卜:")
    for div in recent_divinations:
        user_name = div.user.username if div.user else '匿名用户'
        print(f"  - {user_name}: {div.get_divination_type_display()} ({div.created_at.strftime('%Y-%m-%d %H:%M')})")
    
    # 最近的通知
    recent_notifications = Notification.objects.order_by('-created_at')[:5]
    print("\n🔔 最近通知:")
    for notif in recent_notifications:
        status = "未读" if not notif.is_read else "已读"
        print(f"  - {notif.user.username}: {notif.title} [{status}] ({notif.created_at.strftime('%Y-%m-%d %H:%M')})")

def main():
    """主测试函数"""
    print("🌟 命理大师系统功能测试")
    print("=" * 50)
    
    try:
        test_models()
        test_statistics()
        test_recent_activity()
        
        print("\n" + "=" * 50)
        print("✅ 所有测试完成！系统运行正常")
        
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
