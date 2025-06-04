"""
邮件通知服务
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """邮件服务类"""
    
    @staticmethod
    def send_membership_purchase_confirmation(user, order):
        """发送会员购买确认邮件"""
        try:
            subject = f'命理大师 - 会员购买确认 (订单号: {order.order_id})'
            
            # 渲染HTML邮件模板
            html_message = render_to_string('emails/membership_purchase_confirmation.html', {
                'user': user,
                'order': order,
                'plan': order.plan,
            })
            
            # 纯文本版本
            plain_message = strip_tags(html_message)
            
            # 发送邮件
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'会员购买确认邮件已发送给用户 {user.username}')
            return True
            
        except Exception as e:
            logger.error(f'发送会员购买确认邮件失败: {e}')
            return False
    
    @staticmethod
    def send_membership_activation_notification(user, order):
        """发送会员激活通知邮件"""
        try:
            subject = '命理大师 - VIP会员激活成功'
            
            # 渲染HTML邮件模板
            html_message = render_to_string('emails/membership_activation.html', {
                'user': user,
                'order': order,
                'plan': order.plan,
                'expire_date': user.userprofile.membership_expire_date,
            })
            
            # 纯文本版本
            plain_message = strip_tags(html_message)
            
            # 发送邮件
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'会员激活通知邮件已发送给用户 {user.username}')
            return True
            
        except Exception as e:
            logger.error(f'发送会员激活通知邮件失败: {e}')
            return False
    
    @staticmethod
    def send_membership_expiry_warning(user, days_left):
        """发送会员即将过期警告邮件"""
        try:
            subject = '命理大师 - VIP会员即将过期提醒'
            
            # 渲染HTML邮件模板
            html_message = render_to_string('emails/membership_expiry_warning.html', {
                'user': user,
                'days_left': days_left,
                'expire_date': user.userprofile.membership_expire_date,
            })
            
            # 纯文本版本
            plain_message = strip_tags(html_message)
            
            # 发送邮件
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'会员过期警告邮件已发送给用户 {user.username}')
            return True
            
        except Exception as e:
            logger.error(f'发送会员过期警告邮件失败: {e}')
            return False
    
    @staticmethod
    def send_membership_expired_notification(user):
        """发送会员已过期通知邮件"""
        try:
            subject = '命理大师 - VIP会员已过期'
            
            # 渲染HTML邮件模板
            html_message = render_to_string('emails/membership_expired.html', {
                'user': user,
            })
            
            # 纯文本版本
            plain_message = strip_tags(html_message)
            
            # 发送邮件
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'会员过期通知邮件已发送给用户 {user.username}')
            return True
            
        except Exception as e:
            logger.error(f'发送会员过期通知邮件失败: {e}')
            return False
