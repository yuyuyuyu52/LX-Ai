from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, DivinationRecord, SMSVerification
from .forms import CustomUserCreationForm, UserProfileForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import csv
import json
from datetime import datetime, timedelta
from .sms import generate_verification_code, send_sms_verification
from .sms_views import send_verification_code, check_phone_exists

def home(request):
    """首页视图"""
    from django.db.models import Count
    
    recent_records = DivinationRecord.objects.order_by('-created_at')[:6]
    
    # 统计信息
    total_users = User.objects.count()
    total_divinations = DivinationRecord.objects.count()
    divination_stats = DivinationRecord.objects.values('divination_type').annotate(count=Count('divination_type'))
    context = {
        'recent_records': recent_records,
        'total_users': total_users,
        'total_divinations': total_divinations,
        'divination_stats': divination_stats,
        'page_title': '灵汐命理平台 - 静心观命，感悟人生智慧'
    }
    return render(request, 'core/home.html', context)

def about(request):
    """关于页面"""
    return render(request, 'core/about.html', {'page_title': '关于灵汐命理平台'})

def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('core:profile')
        else:
            messages.error(request, '用户名或密码错误')
    
    return render(request, 'core/login.html', {'page_title': '静心登录 - 灵汐命理平台'})

def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账户 {username} 创建成功！')
            
            # 创建欢迎通知
            from core.models import Notification
            Notification.objects.create(
                user=user,
                title='欢迎加入命理大师！',
                message='感谢您注册命理大师！您现在可以体验八字分析、塔罗占卜、黄历查询等功能。祝您使用愉快！',
                notification_type='success'
            )
            
            # 自动登录
            login(request, user)
            return redirect('core:profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form, 'page_title': '用户注册'})

def user_logout(request):
    """用户登出"""
    logout(request)
    messages.success(request, '您已成功登出')
    return redirect('core:home')

@login_required
def profile(request):
    """用户档案页面"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息更新成功！')
            return redirect('core:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    user_records = DivinationRecord.objects.filter(user=request.user).order_by('-created_at')
    
    # 统计用户的占卜次数
    divination_stats = {}
    for record in user_records:
        div_type = record.get_divination_type_display()
        divination_stats[div_type] = divination_stats.get(div_type, 0) + 1
    
    context = {
        'profile': profile,
        'form': form,
        'user_records': user_records,
        'divination_stats': divination_stats,
        'total_divinations': user_records.count(),
        'page_title': '个人档案'
    }
    return render(request, 'core/profile.html', context)

def stats_api(request):
    """网站统计API"""
    from django.db.models import Count
    from django.contrib.auth.models import User
    
    # 基本统计
    total_users = User.objects.count()
    total_divinations = DivinationRecord.objects.count()
    
    # 占卜类型统计
    divination_stats = DivinationRecord.objects.values('divination_type').annotate(
        count=Count('divination_type')
    ).order_by('-count')
    
    # 最活跃用户
    active_users = User.objects.annotate(
        divination_count=Count('divinationrecord')
    ).filter(divination_count__gt=0).order_by('-divination_count')[:5]
    
    # 最近7天的占卜趋势
    from datetime import datetime, timedelta
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_divinations = DivinationRecord.objects.filter(
        created_at__gte=seven_days_ago
    ).count()
    
    data = {
        'total_users': total_users,
        'total_divinations': total_divinations,
        'recent_divinations': recent_divinations,
        'divination_stats': list(divination_stats),
        'active_users': [
            {
                'username': user.username,
                'divination_count': user.divination_count
            } for user in active_users
        ]
    }
    
    return JsonResponse(data)

@login_required
def search_divination_records(request):
    """搜索和筛选占卜记录"""
    query = request.GET.get('q', '')
    divination_type = request.GET.get('type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    page = request.GET.get('page', 1)
    
    records = DivinationRecord.objects.filter(user=request.user)
    
    # 文本搜索
    if query:
        records = records.filter(
            Q(question__icontains=query) |
            Q(result__icontains=query)
        )
    
    # 类型筛选
    if divination_type:
        records = records.filter(divination_type=divination_type)
    
    # 日期范围筛选
    if date_from:
        records = records.filter(created_at__date__gte=date_from)
    if date_to:
        records = records.filter(created_at__date__lte=date_to)
    
    records = records.order_by('-created_at')
    
    # 分页
    paginator = Paginator(records, 10)
    page_obj = paginator.get_page(page)
    
    return render(request, 'core/search_results.html', {
        'page_title': '搜索结果',
        'page_obj': page_obj,
        'query': query,
        'divination_type': divination_type,
        'date_from': date_from,
        'date_to': date_to,
        'divination_types': DivinationRecord.DIVINATION_TYPES
    })

@login_required
def delete_divination_record(request, record_id):
    """删除占卜记录"""
    if request.method == 'POST':
        try:
            record = DivinationRecord.objects.get(id=record_id, user=request.user)
            record.delete()
            return JsonResponse({'success': True, 'message': '记录已删除'})
        except DivinationRecord.DoesNotExist:
            return JsonResponse({'success': False, 'message': '记录不存在'})
    
    return JsonResponse({'success': False, 'message': '无效请求'})

@login_required
def export_divination_records(request):
    """导出占卜记录为CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="divination_records.csv"'
    response.write('\ufeff')  # UTF-8 BOM
    
    writer = csv.writer(response)
    writer.writerow(['日期', '类型', '问题', '结果', '创建时间'])
    
    records = DivinationRecord.objects.filter(user=request.user).order_by('-created_at')
    for record in records:
        writer.writerow([
            record.created_at.strftime('%Y-%m-%d'),
            record.get_divination_type_display(),
            record.question or '无',
            record.result[:100] + '...' if len(record.result) > 100 else record.result,
            record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

def send_notification(request):
    """发送通知"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        # 这里可以添加邮件或短信通知逻辑
        # 目前只是返回成功响应
        
        return JsonResponse({
            'success': True,
            'message': '通知已发送'
        })
    
    return JsonResponse({'success': False, 'message': '无效请求'})

def get_notifications(request):
    """获取用户通知API"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'})
    
    from core.models import Notification
    
    # 获取基础查询集
    base_notifications = Notification.objects.filter(user=request.user)
    # 计算未读数量（在切片之前）
    unread_count = base_notifications.filter(is_read=False).count()
    # 获取最新的10条通知
    notifications = base_notifications.order_by('-created_at')[:10]
    
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'type': notification.notification_type,
            'is_read': notification.is_read,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count
    })

def mark_notification_read(request):
    """标记通知为已读"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'})
    
    if request.method == 'POST':
        from core.models import Notification
        
        data = json.loads(request.body)
        notification_id = data.get('notification_id')
        
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': '通知不存在'})
    
    return JsonResponse({'success': False, 'error': '请求方法错误'})

def mark_all_notifications_read(request):
    """标记所有通知为已读"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'})
    
    if request.method == 'POST':
        from core.models import Notification
        
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': '请求方法错误'})

def test_verify_page(request):
    """验证码功能测试页面"""
    return render(request, 'core/test_verify.html', {'page_title': '验证码功能测试'})

def verification_test_page(request):
    """完整的验证码功能测试页面"""
    return render(request, 'core/verification_test.html', {'page_title': '验证码功能测试'})
