from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Notification
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = '发送每日运势通知'

    def handle(self, *args, **options):
        today = datetime.now().date()
        
        # 检查今天是否已经发送过运势通知
        recent_notifications = Notification.objects.filter(
            title__contains='今日运势',
            created_at__date=today
        )
        
        if recent_notifications.exists():
            self.stdout.write(self.style.WARNING('今日运势通知已发送'))
            return
        
        # 运势消息模板
        fortune_messages = [
            "今日财运亨通，适合投资理财，但需谨慎选择项目。",
            "今日贵人运强，工作中会遇到有利的合作机会。",
            "今日桃花运旺盛，单身者有机会遇到心仪对象。",
            "今日健康运不错，适合户外运动和锻炼身体。",
            "今日学习运佳，是提升自己技能的好时机。",
            "今日事业运稳定，按部就班完成工作会有好结果。",
            "今日创意灵感丰富，适合从事艺术创作类工作。",
            "今日人际关系和谐，与朋友聚会会带来意外收获。"
        ]
        
        # 为所有活跃用户发送运势通知
        active_users = User.objects.filter(is_active=True)
        sent_count = 0
        
        for user in active_users:
            # 随机选择运势消息
            fortune_message = random.choice(fortune_messages)
            
            Notification.objects.create(
                user=user,
                title=f'今日运势 {today.strftime("%m月%d日")}',
                message=fortune_message,
                notification_type='info'
            )
            sent_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'成功为 {sent_count} 位用户发送今日运势通知')
        )
