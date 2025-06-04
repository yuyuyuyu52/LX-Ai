"""
会员相关视图
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
import json
import uuid
import logging

from .models import MembershipPlan, MembershipOrder, PaymentRecord, UserProfile, Notification
from .forms import MembershipPurchaseForm
from .email_service import EmailService

logger = logging.getLogger(__name__)

def membership_plans(request):
    """会员套餐页面"""
    plans = MembershipPlan.objects.filter(is_active=True).order_by('sort_order', 'price')
    
    # 如果用户已登录，获取用户信息
    user_profile = None
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    context = {
        'plans': plans,
        'user_profile': user_profile,
    }
    return render(request, 'core/membership_plans.html', context)

@login_required
def purchase_membership(request, plan_id):
    """购买会员"""
    plan = get_object_or_404(MembershipPlan, id=plan_id, is_active=True)
    
    if request.method == 'POST':
        form = MembershipPurchaseForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.create_order()
            if order:
                # 跳转到支付页面
                return redirect('membership_payment', order_id=order.order_id)
            else:
                messages.error(request, '创建订单失败，请重试')
        else:
            messages.error(request, '表单验证失败，请检查输入信息')
    else:
        form = MembershipPurchaseForm(initial={'plan_id': plan_id}, user=request.user)
    
    context = {
        'plan': plan,
        'form': form,
    }
    return render(request, 'core/purchase_membership.html', context)

@login_required
def membership_payment(request, order_id):
    """支付页面"""
    order = get_object_or_404(MembershipOrder, order_id=order_id, user=request.user)
    
    # 检查订单状态
    if order.status != 'pending':
        messages.error(request, '订单状态异常')
        return redirect('membership_plans')
    
    # 检查订单是否过期
    if order.is_expired():
        order.status = 'expired'
        order.save()
        messages.error(request, '订单已过期，请重新下单')
        return redirect('membership_plans')
    
    context = {
        'order': order,
    }
    return render(request, 'core/membership_payment.html', context)

@login_required
@require_http_methods(["POST"])
def process_payment(request, order_id):
    """处理支付"""
    order = get_object_or_404(MembershipOrder, order_id=order_id, user=request.user)
    
    if order.status != 'pending':
        return JsonResponse({'success': False, 'message': '订单状态异常'})
    
    if order.is_expired():
        order.status = 'expired'
        order.save()
        return JsonResponse({'success': False, 'message': '订单已过期'})
    
    payment_method = order.payment_method
    
    try:
        if payment_method == 'mock':
            # 模拟支付（仅开发环境）
            if settings.DEBUG:
                success = simulate_payment(order)
            else:
                return JsonResponse({'success': False, 'message': '生产环境不支持模拟支付'})
        elif payment_method == 'wechat':
            success = process_wechat_payment(order)
        elif payment_method == 'alipay':
            success = process_alipay_payment(order)
        else:
            return JsonResponse({'success': False, 'message': '不支持的支付方式'})
        
        if success:
            return JsonResponse({
                'success': True, 
                'message': '支付成功',
                'redirect_url': '/membership/success/'
            })
        else:
            return JsonResponse({'success': False, 'message': '支付失败，请重试'})
            
    except Exception as e:
        logger.error(f"支付处理异常: {e}")
        return JsonResponse({'success': False, 'message': '支付处理异常，请联系客服'})

def simulate_payment(order):
    """模拟支付（仅用于开发测试）"""
    try:
        # 模拟支付成功
        order.status = 'paid'
        order.payment_time = timezone.now()
        order.trade_no = f"MOCK_{uuid.uuid4().hex[:16].upper()}"
        order.save()
        
        # 创建支付记录
        PaymentRecord.objects.create(
            order=order,
            payment_method=order.payment_method,
            amount=order.amount,
            trade_no=order.trade_no,
            payment_data={'mock': True, 'timestamp': str(timezone.now())}
        )
        
        # 激活会员
        order.activate_membership()
        
        logger.info(f"模拟支付成功: 订单{order.order_id}")
        return True
        
    except Exception as e:
        logger.error(f"模拟支付失败: {e}")
        return False

def process_wechat_payment(order):
    """处理微信支付"""
    # TODO: 集成微信支付API
    # 这里应该调用微信支付API创建支付订单
    # 返回支付链接或二维码给前端
    logger.info(f"微信支付处理: 订单{order.order_id}")
    return False

def process_alipay_payment(order):
    """处理支付宝支付"""
    # TODO: 集成支付宝API
    # 这里应该调用支付宝API创建支付订单
    # 返回支付链接给前端
    logger.info(f"支付宝支付处理: 订单{order.order_id}")
    return False

@login_required
def membership_success(request):
    """支付成功页面"""
    return render(request, 'core/membership_success.html')

@login_required
def membership_orders(request):
    """我的订单"""
    orders = MembershipOrder.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'core/membership_orders.html', context)

@login_required
def membership_status(request):
    """会员状态页面"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # 获取最近的订单
    recent_orders = MembershipOrder.objects.filter(
        user=request.user, 
        status='paid'
    ).order_by('-payment_time')[:5]
    
    context = {
        'user_profile': user_profile,
        'recent_orders': recent_orders,
    }
    return render(request, 'core/membership_status.html', context)

@csrf_exempt
def payment_callback(request):
    """支付回调处理"""
    if request.method != 'POST':
        return JsonResponse({'success': False})
    
    try:
        # 处理支付回调
        # 这里根据不同的支付方式处理回调数据
        payment_method = request.POST.get('payment_method', '')
        
        if payment_method == 'wechat':
            return handle_wechat_callback(request)
        elif payment_method == 'alipay':
            return handle_alipay_callback(request)
        else:
            return JsonResponse({'success': False, 'message': '未知支付方式'})
            
    except Exception as e:
        logger.error(f"支付回调处理异常: {e}")
        return JsonResponse({'success': False})

def handle_wechat_callback(request):
    """处理微信支付回调"""
    # TODO: 实现微信支付回调验证和处理
    return JsonResponse({'success': True})

def handle_alipay_callback(request):
    """处理支付宝回调"""
    # TODO: 实现支付宝回调验证和处理
    return JsonResponse({'success': True})

def check_membership_status(request):
    """检查会员状态API"""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': True, 
                'data': {
                    'is_vip': False,
                    'membership_type': 'free',
                    'expire_date': None,
                }
            })
        
        user_profile = UserProfile.objects.get(user=request.user)
        is_vip = user_profile.is_vip()
        
        data = {
            'is_vip': is_vip,
            'membership_type': user_profile.membership,
            'expire_date': user_profile.membership_expire_date.isoformat() if user_profile.membership_expire_date else None,
        }
        
        return JsonResponse({'success': True, 'data': data})
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户档案不存在'})
    except Exception as e:
        logger.error(f"检查会员状态异常: {e}")
        return JsonResponse({'success': False, 'message': '服务器错误'})
