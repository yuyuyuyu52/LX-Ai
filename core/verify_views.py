from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SMSVerification
from .sms import generate_verification_code
import logging

logger = logging.getLogger(__name__)

def verify_test_page(request):
    """显示验证码测试页面"""
    return render(request, 'core/verify_test.html')

@csrf_exempt
def direct_sms_test(request):
    """直接发送短信验证码的测试方法"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '仅支持POST请求'})
    
    try:
        phone_number = request.POST.get('phone')
        if not phone_number:
            return JsonResponse({'success': False, 'message': '请提供手机号码'})
            
        import re
        if not re.match(r'^1[3-9]\d{9}$', phone_number):
            return JsonResponse({'success': False, 'message': '请输入有效的手机号码'})
        
        verification_code = generate_verification_code()
        
        # 记录到数据库
        SMSVerification.objects.create(
            phone_number=phone_number,
            code=verification_code
        )
        
        logger.info(f"测试环境: 为手机号 {phone_number} 生成验证码 {verification_code}")
        
        # 仅用于测试，在生产环境不应返回验证码
        return JsonResponse({
            'success': True, 
            'message': '验证码已发送',
            'code': verification_code
        })
        
    except Exception as e:
        logger.exception("发送测试验证码出错")
        return JsonResponse({'success': False, 'message': f'发送验证码失败: {str(e)}'})

@csrf_exempt
def verify_sms_test(request):
    """验证短信验证码的测试方法"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '仅支持POST请求'})
    
    try:
        phone_number = request.POST.get('phone')
        code = request.POST.get('code')
        
        if not phone_number or not code:
            return JsonResponse({'valid': False, 'message': '请提供手机号码和验证码'})
        
        # 查询最新的验证码记录
        try:
            verification = SMSVerification.objects.filter(
                phone_number=phone_number,
                is_used=False
            ).latest('created_at')
            
            if not verification.is_valid():
                return JsonResponse({'valid': False, 'message': '验证码已过期'})
                
            if verification.code != code:
                return JsonResponse({'valid': False, 'message': '验证码错误'})
                
            # 验证通过，标记为已使用
            verification.is_used = True
            verification.save()
            
            return JsonResponse({'valid': True, 'message': '验证成功'})
            
        except SMSVerification.DoesNotExist:
            return JsonResponse({'valid': False, 'message': '验证码不存在或已使用'})
        
    except Exception as e:
        logger.exception("验证测试验证码出错")
        return JsonResponse({'valid': False, 'message': f'验证失败: {str(e)}'})
