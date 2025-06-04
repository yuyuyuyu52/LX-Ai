from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import logging
from .models import SMSVerification
from .sms import generate_verification_code, send_sms_verification

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def sms_test_page(request):
    """测试短信验证码页面"""
    return render(request, 'core/sms_test.html')

@require_POST
def test_send_sms(request):
    """测试发送短信验证码功能"""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        
        # 验证手机号格式
        import re
        if not re.match(r'^1[3-9]\d{9}$', phone_number):
            return JsonResponse({'success': False, 'message': '请输入有效的手机号码'})
        
        # 生成验证码
        verification_code = generate_verification_code()
        
        # 在正式环境下，这里应该调用真实的短信发送服务
        # 但在测试环境下，我们直接返回验证码
        
        # 记录到数据库
        SMSVerification.objects.create(
            phone_number=phone_number,
            code=verification_code
        )
        
        logger.info(f"测试模式：发送验证码 {verification_code} 到手机号 {phone_number}")
        
        # 在测试页面中返回验证码（仅测试用途）
        return JsonResponse({
            'success': True, 
            'message': '验证码已发送', 
            'code': verification_code
        })
    except Exception as e:
        logger.error(f"发送测试验证码出错: {str(e)}")
        return JsonResponse({'success': False, 'message': f'发送验证码失败: {str(e)}'})

@require_POST
def test_verify_sms(request):
    """测试验证短信验证码功能"""
    try:
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        code = data.get('code')
        
        # 查询最新的验证码记录
        try:
            sms_verification = SMSVerification.objects.filter(
                phone_number=phone_number,
                is_used=False
            ).latest('created_at')
            
            if not sms_verification.is_valid():
                return JsonResponse({'valid': False, 'message': '验证码已过期'})
            
            if sms_verification.code != code:
                return JsonResponse({'valid': False, 'message': '验证码错误'})
            
            # 验证成功，标记为已使用
            sms_verification.is_used = True
            sms_verification.save()
            
            return JsonResponse({'valid': True, 'message': '验证码验证成功'})
            
        except SMSVerification.DoesNotExist:
            return JsonResponse({'valid': False, 'message': '验证码不存在或已被使用'})
            
    except Exception as e:
        logger.error(f"验证测试验证码出错: {str(e)}")
        return JsonResponse({'valid': False, 'message': f'验证失败: {str(e)}'})
