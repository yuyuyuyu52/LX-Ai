from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, DivinationRecord, Notification

class CustomAdminSite(admin.AdminSite):
    site_header = '命理大师管理后台'
    site_title = '命理大师'
    index_title = '系统管理'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_view(self.stats_view), name='admin_stats'),
        ]
        return custom_urls + urls
    
    def stats_view(self, request):
        """统计数据视图"""
        # 基本统计
        total_users = User.objects.count()
        total_divinations = DivinationRecord.objects.count()
        total_notifications = Notification.objects.count()
        
        # 今日数据
        today = timezone.now().date()
        today_users = User.objects.filter(date_joined__date=today).count()
        today_divinations = DivinationRecord.objects.filter(created_at__date=today).count()
        
        # 占卜类型统计
        divination_stats = DivinationRecord.objects.values('divination_type').annotate(
            count=Count('divination_type')
        ).order_by('-count')
        
        # 最近7天的用户活动
        last_7_days = []
        for i in range(7):
            date = today - timedelta(days=i)
            day_divinations = DivinationRecord.objects.filter(created_at__date=date).count()
            day_users = User.objects.filter(date_joined__date=date).count()
            last_7_days.append({
                'date': date,
                'divinations': day_divinations,
                'users': day_users
            })
        
        # 热门用户（占卜次数最多）
        top_users = User.objects.annotate(
            divination_count=Count('divinationrecord')
        ).filter(divination_count__gt=0).order_by('-divination_count')[:10]
        
        # 未读通知统计
        unread_notifications = Notification.objects.filter(is_read=False).count()
        
        context = {
            'title': '数据统计',
            'total_users': total_users,
            'total_divinations': total_divinations,
            'total_notifications': total_notifications,
            'today_users': today_users,
            'today_divinations': today_divinations,
            'divination_stats': divination_stats,
            'last_7_days': reversed(last_7_days),
            'top_users': top_users,
            'unread_notifications': unread_notifications,
        }
        
        return render(request, 'admin/stats.html', context)

# 创建自定义admin站点实例
admin_site = CustomAdminSite(name='custom_admin')
