from django.urls import path
from . import views

app_name = 'chinese_calendar'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('today/', views.today_fortune, name='today'),
    path('api/date/<str:date_str>/', views.date_info_api, name='date_api'),
    path('api/calendar/<str:date_str>/', views.calendar_api, name='calendar_api'),
]
