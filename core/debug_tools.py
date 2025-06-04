from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import logging

from .sms import generate_verification_code
from .models import SMSVerification

logger = logging.getLogger(__name__)

def sms_debug_page(request):
    """显示验证码调试页面"""
    return render(request, 'core/sms_debug.html')

def verification_debug_page(request):
    """验证码调试页面"""
    return render(request, 'core/verification_debug.html')

@csrf_exempt
def direct_generate_code(request):
    """生成验证码并直接返回 - 支持GET和POST请求"""
    if request.method == 'GET':
        return JsonResponse({'success': False, 'message': '请使用POST请求'})
        
    try:
        phone = request.POST.get('phone', '').strip()
        
        if not phone:
            return JsonResponse({'success': False, 'message': '请提供手机号码'})
            
        # 严格验证手机号格式
        import re
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return JsonResponse({'success': False, 'message': '请输入有效的11位手机号码，以1开头'})
        
        # 检查发送频率限制（同一手机号1分钟内最多发送1次）
        from django.utils import timezone
        from datetime import timedelta
        
        recent_sms = SMSVerification.objects.filter(
            phone_number=phone,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).exists()
        
        if recent_sms:
            return JsonResponse({
                'success': False, 
                'message': '验证码发送过于频繁，请1分钟后再试'
            })
        
        # 检查当天发送次数限制（同一手机号每天最多10次）
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = SMSVerification.objects.filter(
            phone_number=phone,
            created_at__gte=today_start
        ).count()
        
        if today_count >= 10:
            return JsonResponse({
                'success': False, 
                'message': '今日验证码发送次数已达上限，请明天再试'
            })
        
        # 生成验证码
        verification_code = generate_verification_code()
        
        # 获取客户端IP地址
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        
        client_ip = get_client_ip(request)
        
        # 保存到数据库
        SMSVerification.objects.create(
            phone_number=phone,
            code=verification_code,
            ip_address=client_ip
        )
        
        logger.info(f"验证码生成成功: 手机号={phone}, 验证码={verification_code}")
        
        return JsonResponse({
            'success': True, 
            'message': '验证码已发送，请查收短信',
            'code': verification_code  # 开发环境下返回验证码
        })
        
    except Exception as e:
        logger.exception("生成验证码出错")
        return JsonResponse({
            'success': False, 
            'message': '系统繁忙，请稍后再试'
        })
