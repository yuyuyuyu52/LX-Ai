"""
清理过期会员的管理命令
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import UserProfile, Notification


class Command(BaseCommand):
    help = '清理过期会员并发送通知'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅显示将要处理的数据，不实际执行',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        current_time = timezone.now()
        
        # 查找过期会员
        expired_members = UserProfile.objects.filter(
            membership='vip',
            membership_expire_date__lt=current_time
        )
        
        self.stdout.write(f'找到 {expired_members.count()} 个过期会员')
        
        if dry_run:
            for profile in expired_members:
                self.stdout.write(
                    f'[DRY RUN] 用户 {profile.user.username} 会员已过期 '
                    f'(到期时间: {profile.membership_expire_date})'
                )
            return
        
        # 处理过期会员
        processed_count = 0
        for profile in expired_members:
            # 更新会员状态
            profile.membership = 'free'
            old_expire_date = profile.membership_expire_date
            profile.membership_expire_date = None
            profile.save()
            
            # 创建过期通知
            Notification.objects.get_or_create(
                user=profile.user,
                title='VIP会员已过期',
                defaults={
                    'message': f'您的VIP会员已于{old_expire_date.strftime("%Y年%m月%d日")}过期，请续费以继续享受专属服务。',
                    'notification_type': 'warning'
                }
            )
            
            processed_count += 1
            self.stdout.write(
                f'处理用户 {profile.user.username} 会员过期 '
                f'(到期时间: {old_expire_date})'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'成功处理 {processed_count} 个过期会员')
        )
        
        # 查找即将过期的会员（7天内）
        from datetime import timedelta
        warn_date = current_time + timedelta(days=7)
        
        expiring_members = UserProfile.objects.filter(
            membership='vip',
            membership_expire_date__gt=current_time,
            membership_expire_date__lt=warn_date
        )
        
        self.stdout.write(f'找到 {expiring_members.count()} 个即将过期的会员')
        
        # 发送即将过期通知
        warning_count = 0
        for profile in expiring_members:
            days_left = (profile.membership_expire_date - current_time).days
            
            # 检查是否已发送过通知（避免重复发送）
            existing_notification = Notification.objects.filter(
                user=profile.user,
                title='VIP会员即将过期',
                created_at__date=current_time.date()
            ).exists()
            
            if not existing_notification:
                if not dry_run:
                    Notification.objects.create(
                        user=profile.user,
                        title='VIP会员即将过期',
                        message=f'您的VIP会员将在{days_left}天后过期，请及时续费以继续享受专属服务。',
                        notification_type='info'
                    )
                
                warning_count += 1
                self.stdout.write(
                    f'{("[DRY RUN] " if dry_run else "")}发送过期提醒给用户 {profile.user.username} '
                    f'(剩余{days_left}天)'
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'发送 {warning_count} 个过期提醒通知')
        )
