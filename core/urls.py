from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),    path('api/stats/', views.stats_api, name='stats_api'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('search/', views.search_divination_records, name='search_records'),
    path('delete-record/<int:record_id>/', views.delete_divination_record, name='delete_record'),
    path('export-records/', views.export_divination_records, name='export_records'),
    path('send-notification/', views.send_notification, name='send_notification'),
]
