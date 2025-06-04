from django.db import models

class BaziElement(models.Model):
    name = models.CharField(max_length=20)  # 甲、乙、丙、丁等
    element_type = models.CharField(max_length=10, choices=[
        ('tiangan', '天干'),
        ('dizhi', '地支')
    ])
    wuxing = models.CharField(max_length=10, choices=[
        ('jin', '金'),
        ('mu', '木'),
        ('shui', '水'),
        ('huo', '火'),
        ('tu', '土')
    ])
    
    def __str__(self):
        return self.name
