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

class TarotCard(models.Model):
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    card_number = models.IntegerField()
    suit = models.CharField(max_length=20, choices=[
        ('major', '大阿卡纳'),
        ('wands', '权杖'),
        ('cups', '圣杯'),
        ('swords', '宝剑'),
        ('pentacles', '金币')
    ])
    upright_meaning = models.TextField()
    reversed_meaning = models.TextField()
    image = models.ImageField(upload_to='tarot_cards/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class IChingHexagram(models.Model):
    number = models.IntegerField(unique=True)  # 1-64
    name = models.CharField(max_length=20)
    chinese_name = models.CharField(max_length=10)
    binary = models.CharField(max_length=6)  # 111111 形式
    meaning = models.TextField()
    judgment = models.TextField()  # 彖辞
    image = models.TextField()     # 象辞
    
    def __str__(self):
        return f"{self.number}. {self.chinese_name} {self.name}"
