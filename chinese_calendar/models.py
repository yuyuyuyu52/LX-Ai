from django.db import models

class ChineseCalendarDay(models.Model):
    date = models.DateField(unique=True)
    lunar_year = models.CharField(max_length=20)    # 农历年
    lunar_month = models.CharField(max_length=20)   # 农历月
    lunar_day = models.CharField(max_length=20)     # 农历日
    tiangan = models.CharField(max_length=10)       # 天干
    dizhi = models.CharField(max_length=10)         # 地支
    constellation = models.CharField(max_length=20) # 星座
    suitable_activities = models.TextField(blank=True)  # 宜
    avoid_activities = models.TextField(blank=True)     # 忌
    
    def __str__(self):
        return f"{self.date} - {self.lunar_year}{self.lunar_month}{self.lunar_day}"

class SolarTerm(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateField()
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.date}"
