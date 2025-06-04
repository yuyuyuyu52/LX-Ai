from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json
from .models import UserProfile, SMSVerification
from .sms import generate_verification_code, send_sms_verification

@csrf_exempt
@require_POST
def send_verification_code(request):
    """发送手机验证码"""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        
        # 验证手机号格式
        import re
        if not re.match(r'^1[3-9]\d{9}$', phone_number):
            return JsonResponse({'success': False, 'message': '请输入有效的手机号码'})
        
        # 检查手机号是否已被注册
        if UserProfile.objects.filter(phone_number=phone_number, phone_verified=True).exists():
            return JsonResponse({'success': False, 'message': '该手机号已被注册'})
        
        # 限制验证码发送频率（1分钟内只能发送一次）
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if SMSVerification.objects.filter(phone_number=phone_number, created_at__gt=one_minute_ago).exists():
            return JsonResponse({'success': False, 'message': '请等待1分钟后再次获取验证码'})
        
        # 生成并发送验证码
        verification_code = generate_verification_code()
        send_success = send_sms_verification(phone_number, verification_code)
        
        if send_success:
            # 保存验证码记录
            SMSVerification.objects.create(
                phone_number=phone_number,
                code=verification_code
            )
            return JsonResponse({'success': True, 'message': '验证码已发送'})
        else:
            return JsonResponse({'success': False, 'message': '验证码发送失败，请稍后再试'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'发送验证码失败: {str(e)}'})

def check_phone_exists(request):
    """检查手机号是否已注册"""
    phone_number = request.GET.get('phone_number', '')
    
    if UserProfile.objects.filter(phone_number=phone_number, phone_verified=True).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
