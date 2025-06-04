from django.urls import path
from . import views
from . import test_sms_views
from . import verify_views
from . import debug_tools
from . import membership_views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('api/check-phone/', views.check_phone_exists, name='check_phone_exists'),
    # 测试路由
    path('test-sms/', test_sms_views.sms_test_page, name='sms_test_page'),
    path('test-sms-send/', test_sms_views.test_send_sms, name='test_send_sms'),
    path('test-sms-verify/', test_sms_views.test_verify_sms, name='test_verify_sms'),
    # 简化版验证码测试
    path('verify-test/', verify_views.verify_test_page, name='verify_test_page'),
    path('direct-sms-test/', verify_views.direct_sms_test, name='direct_sms_test'),
    path('verify-sms-test/', verify_views.verify_sms_test, name='verify_sms_test'),
    # 简单调试工具
    path('sms-debug/', debug_tools.sms_debug_page, name='sms_debug_page'),
    path('get-code/', debug_tools.direct_generate_code, name='generate_code'),    
    path('test-verify/', views.test_verify_page, name='test_verify_page'),
    path('verification-test/', views.verification_test_page, name='verification_test_page'),
    path('api/stats/', views.stats_api, name='stats_api'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('search/', views.search_divination_records, name='search_records'),
    path('delete-record/<int:record_id>/', views.delete_divination_record, name='delete_record'),
    path('export-records/', views.export_divination_records, name='export_records'),
    path('send-notification/', views.send_notification, name='send_notification'),
    # 调试页面
    path('debug-verification/', debug_tools.verification_debug_page, name='verification_debug_page'),
    # 会员相关路由
    path('membership/', membership_views.membership_plans, name='membership_plans'),
    path('membership/purchase/<int:plan_id>/', membership_views.purchase_membership, name='purchase_membership'),
    path('membership/payment/<str:order_id>/', membership_views.membership_payment, name='membership_payment'),
    path('membership/process-payment/<str:order_id>/', membership_views.process_payment, name='process_payment'),
    path('membership/success/', membership_views.membership_success, name='membership_success'),
    path('membership/orders/', membership_views.membership_orders, name='membership_orders'),
    path('membership/status/', membership_views.membership_status, name='membership_status'),
    path('api/membership/status/', membership_views.check_membership_status, name='check_membership_status'),
    path('payment/callback/', membership_views.payment_callback, name='payment_callback'),
]
