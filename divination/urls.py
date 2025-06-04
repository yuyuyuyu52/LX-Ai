from django.urls import path
from . import views

app_name = 'divination'

urlpatterns = [
    path('bazi/', views.bazi_analysis, name='bazi'),
    path('meihua/', views.meihua_yishu, name='meihua'),
    path('bazi-marriage/', views.bazi_marriage, name='bazi_marriage'),
    path('daily-fortune/', views.daily_fortune, name='daily_fortune'),
    path('api/bazi/', views.bazi_api, name='bazi_api'),
    path('api/meihua/', views.meihua_api, name='meihua_api'),
    path('api/bazi-marriage/', views.bazi_marriage_api, name='bazi_marriage_api'),
    path('api/daily-fortune/', views.daily_fortune_api, name='daily_fortune_api'),
]
