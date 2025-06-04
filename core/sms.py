import random
import logging
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)

def generate_verification_code():
    """生成六位数字验证码"""
    return str(random.randint(100000, 999999))

def send_sms_verification(phone_number, code):
    """
    发送短信验证码
    
    这是一个模拟实现，在实际生产环境中，您需要替换为真实的短信服务商API
    如阿里云、腾讯云等短信服务
    """
    logger.info(f"发送验证码 {code} 到手机号 {phone_number}")
    # 在这里调用真实的短信API，例如：
    # 阿里云短信示例代码:
    # from aliyunsdkcore.client import AcsClient
    # from aliyunsdkcore.request import CommonRequest
    # client = AcsClient(settings.ALIYUN_ACCESS_KEY, settings.ALIYUN_ACCESS_SECRET, 'cn-hangzhou')
    # request = CommonRequest()
    # request.set_domain('dysmsapi.aliyuncs.com')
    # request.set_version('2017-05-25')
    # request.set_action_name('SendSms')
    # request.add_query_param('PhoneNumbers', phone_number)
    # request.add_query_param('SignName', settings.SMS_SIGN_NAME)
    # request.add_query_param('TemplateCode', settings.SMS_TEMPLATE_CODE)
    # request.add_query_param('TemplateParam', '{"code":"' + code + '"}')
    # response = client.do_action_with_exception(request)
    # return response
    
    # 模拟返回成功
    return True
