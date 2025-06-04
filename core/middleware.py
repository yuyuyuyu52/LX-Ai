"""
Core应用中间件
"""
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse
from .models import UserProfile


class MembershipMiddleware:
    """会员状态检查中间件"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """在视图处理前检查会员状态"""
        # 只对已登录用户进行检查
        if not request.user.is_authenticated:
            return None
            
        # 跳过管理后台和静态文件
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
            
        # 获取用户档案
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # 如果用户档案不存在，创建一个
            profile = UserProfile.objects.create(user=request.user)
        
        # 检查会员状态是否过期
        if profile.membership == 'vip' and profile.membership_expire_date:
            if timezone.now() > profile.membership_expire_date:
                # 会员已过期，更新状态
                profile.membership = 'free'
                profile.membership_expire_date = None
                profile.save()
                
                # 创建过期通知
                from .models import Notification
                Notification.objects.get_or_create(
                    user=request.user,
                    title='会员已过期',
                    message='您的VIP会员已过期，请续费以继续享受专属服务。',
                    notification_type='warning'
                )
        
        # 将会员状态添加到请求中，方便视图使用
        request.is_vip = profile.is_vip()
        request.user_profile = profile
        
        return None


class VIPRequiredMixin:
    """需要VIP权限的视图混入类"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:login')
            
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            
        if not profile.is_vip():
            # 重定向到会员购买页面
            return redirect('core:membership_plans')
            
        return super().dispatch(request, *args, **kwargs)
