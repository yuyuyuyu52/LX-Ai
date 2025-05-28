from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Notification

class Command(BaseCommand):
    help = '创建示例通知数据'

    def handle(self, *args, **options):
        # 为所有用户创建欢迎通知
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('没有用户，跳过创建通知'))
            return
        
        for user in users:
            # 检查是否已经有欢迎通知
            if not Notification.objects.filter(user=user, title='欢迎使用命理大师').exists():
                Notification.objects.create(
                    user=user,
                    title='欢迎使用命理大师',
                    message='感谢您注册命理大师！您可以开始体验八字分析、塔罗占卜等功能。',
                    notification_type='success'
                )
                self.stdout.write(f'为用户 {user.username} 创建欢迎通知')
        
        # 创建一些系统通知示例
        if users.exists():
            admin_user = users.first()
            
            # 功能更新通知
            if not Notification.objects.filter(title='新功能上线').exists():
                Notification.objects.create(
                    user=admin_user,
                    title='新功能上线',
                    message='我们新增了通知系统和搜索功能，快来体验吧！',
                    notification_type='info'
                )
            
            # 维护通知
            if not Notification.objects.filter(title='系统维护提醒').exists():
                Notification.objects.create(
                    user=admin_user,
                    title='系统维护提醒',
                    message='系统将在今晚23:00-01:00进行例行维护，期间可能影响部分功能使用。',
                    notification_type='warning'
                )
        
        self.stdout.write(self.style.SUCCESS('示例通知创建完成！'))
