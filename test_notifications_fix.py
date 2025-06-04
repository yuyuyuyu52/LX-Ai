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
from core.models import UserProfile, Notification

def test_notifications_api():
    print('🔍 测试通知API修复...')
    
    # 创建测试客户端
    client = Client()
    
    # 获取或创建测试用户
    user, created = User.objects.get_or_create(username='notification_test', defaults={'password': 'testpass123'})
    if created:
        UserProfile.objects.create(user=user, nickname='通知测试用户')
        print('✅ 创建测试用户')
    
    # 创建一些测试通知
    for i in range(3):
        Notification.objects.get_or_create(
            user=user,
            title=f'测试通知 {i+1}',
            defaults={'message': f'这是第{i+1}个测试通知', 'notification_type': 'info'}
        )
    
    # 登录用户
    client.force_login(user)
    
    # 测试通知API
    response = client.get('/api/notifications/')
    print(f'✅ 通知API响应状态: {response.status_code}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ 通知数量: {len(data.get("notifications", []))}')
        print(f'✅ 未读数量: {data.get("unread_count", 0)}')
        print('🎉 通知API修复成功！')
        return True
    else:
        print(f'❌ 通知API错误: {response.content}')
        return False

if __name__ == '__main__':
    success = test_notifications_api()
    if success:
        print('\n🎊 所有修复验证完成！系统运行正常！')
    else:
        print('\n⚠️ 发现问题，需要进一步检查')
