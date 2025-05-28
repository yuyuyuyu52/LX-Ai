#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from django.db.models import Count

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
        print(f"✅ 创建禅意占卜记录: {divination}")
    else:
        print(f"ℹ️ 禅意占卜记录已存在: {divination}")
    
    # 测试通知
    notification, created = Notification.objects.get_or_create(
        user=test_user,
        title='灵汐平台温馨提醒',
        defaults={
            'message': '静心观命，感悟人生智慧。愿您在灵汐平台找到内心的宁静与指引。',
            'notification_type': 'info'
        }
    )
    
    if created:
        print(f"✅ 创建禅意通知: {notification}")
    else:
        print(f"ℹ️ 禅意通知已存在: {notification}")

def test_statistics():
    """测试统计功能"""
    print("\n📊 灵汐平台统计信息:")
    
    total_users = User.objects.count()
    total_divinations = DivinationRecord.objects.count()
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    
    print(f"🧘 平台用户数: {total_users}")
    print(f"🌙 占卜咨询次数: {total_divinations}")
    print(f"💌 温馨提醒数: {total_notifications}")
    print(f"📬 未读提醒: {unread_notifications}")
    
    # 占卜类型统计
    print("\n🎯 禅意占卜类型分布:")
    divination_stats = DivinationRecord.objects.values('divination_type').annotate(
        count=Count('divination_type')
    ).order_by('-count')
    
    for stat in divination_stats:
        type_names = {
            'bazi': '八字分析 - 探寻命理根源',
            'tarot': '塔罗占卜 - 内在智慧对话',
            'meihua': '梅花易数 - 见微知著',
            'yijing': '易经卜卦 - 天地阴阳变化'
        }
        type_name = type_names.get(stat['divination_type'], stat['divination_type'])
        print(f"  🕯️ {type_name}: {stat['count']} 次")

def test_recent_activity():
    """测试最近活动"""
    print("\n📅 近期灵汐活动:")
    
    # 最近的占卜记录
    recent_divinations = DivinationRecord.objects.order_by('-created_at')[:5]
    print("🌸 最近禅意咨询:")
    for div in recent_divinations:
        user_name = div.user.username if div.user else '静心访客'
        divination_type_display = {
            'bazi': '八字分析',
            'tarot': '塔罗占卜', 
            'meihua': '梅花易数',
            'yijing': '易经卜卦'
        }.get(div.divination_type, div.divination_type)
        print(f"  🍃 {user_name}: {divination_type_display} ({div.created_at.strftime('%Y-%m-%d %H:%M')})")
    
    # 最近的通知
    recent_notifications = Notification.objects.order_by('-created_at')[:5]
    print("\n🔔 最近温馨提醒:")
    for notif in recent_notifications:
        status = "待读" if not notif.is_read else "已阅"
        print(f"  💫 {notif.user.username}: {notif.title} [{status}] ({notif.created_at.strftime('%Y-%m-%d %H:%M')})")

def test_zen_features():
    """测试禅意特色功能"""
    print("\n🌿 禅意特色功能测试:")
    
    # 测试不同时间的用户活跃度
    now = datetime.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    
    today_divinations = DivinationRecord.objects.filter(created_at__date=today).count()
    yesterday_divinations = DivinationRecord.objects.filter(created_at__date=yesterday).count()
    week_divinations = DivinationRecord.objects.filter(created_at__date__gte=week_ago).count()
    
    print(f"  🌅 今日静心咨询: {today_divinations} 次")
    print(f"  🌇 昨日静心咨询: {yesterday_divinations} 次") 
    print(f"  📆 本周静心咨询: {week_divinations} 次")
    
    # 测试用户档案完整度
    profiles_with_birth = UserProfile.objects.filter(birth_date__isnull=False).count()
    total_profiles = UserProfile.objects.count()
    
    if total_profiles > 0:
        completeness = (profiles_with_birth / total_profiles) * 100
        print(f"  📝 用户档案完整度: {completeness:.1f}%")
    else:
        print(f"  📝 用户档案完整度: 0%")

def test_zen_messages():
    """测试禅意消息系统"""
    print("\n💭 禅意消息测试:")
    
    zen_messages = [
        "静心观命，感悟人生智慧",
        "天地有大美而不言，四时有明法而不议",
        "心如止水，命运自现",
        "禅心一片，洞察万象",
        "宁静致远，智慧如泉"
    ]
    
    for i, message in enumerate(zen_messages, 1):
        print(f"  🕯️ 禅语 {i}: {message}")

def main():
    """主测试函数"""
    print("🌙 灵汐命理平台系统测试")
    print("═" * 50)
    print("静心观命，感悟人生智慧")
    print("═" * 50)
    
    try:
        test_models()
        test_statistics()
        test_recent_activity()
        test_zen_features()
        test_zen_messages()
        
        print("\n" + "═" * 50)
        print("✨ 所有测试完成！灵汐平台运行如意")
        print("🌸 愿您在这里找到内心的宁静与指引")
        print("═" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试遇到障碍: {e}")
        print("🙏 请检查系统配置，静心重试")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
