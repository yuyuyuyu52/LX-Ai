"""
Core应用装饰器
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


def vip_required(view_func):
    """需要VIP会员权限的装饰器"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        if not profile.is_vip():
            messages.warning(request, '此功能需要VIP会员权限，请先购买会员。')
            return redirect('core:membership_plans')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def membership_info(view_func):
    """为视图添加会员信息的装饰器"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=request.user)
            
            # 添加会员信息到请求中
            request.is_vip = profile.is_vip()
            request.user_profile = profile
            
            # 检查会员是否即将过期（7天内）
            if profile.is_vip() and profile.membership_expire_date:
                from django.utils import timezone
                from datetime import timedelta
                
                days_left = (profile.membership_expire_date - timezone.now()).days
                if 0 < days_left <= 7:
                    messages.info(request, f'您的VIP会员将在{days_left}天后过期，请及时续费。')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def check_usage_limit(usage_type='general', limit_per_day=10):
    """检查使用次数限制的装饰器"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = request.user.userprofile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=request.user)
            
            # VIP用户无限制
            if profile.is_vip():
                return view_func(request, *args, **kwargs)
            
            # 检查今日使用次数
            from django.utils import timezone
            from .models import DivinationRecord
            
            today = timezone.now().date()
            today_usage = DivinationRecord.objects.filter(
                user=request.user,
                created_at__date=today
            ).count()
            
            if today_usage >= limit_per_day:
                messages.warning(
                    request, 
                    f'您今日已使用{today_usage}次，达到每日限制。升级VIP享受无限次使用。'
                )
                return redirect('core:membership_plans')
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
