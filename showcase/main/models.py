from django.db import models
from django.utils import timezone
# Create your models here.


class ContactResponse(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Otp(models.Model):
    
    email = models.EmailField()
    otp = models.CharField(max_length=7)
    sent_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

class Stocks(models.Model):
    stock_name = models.CharField(max_length=100)
    stock_url = models.URLField()
    high_price = models.CharField(max_length=100, default=0)
    low_price = models.CharField(max_length=100, default=0)
    returns = models.CharField(max_length=100, default='0.00%')
    last_fetched_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Stocks"
        ordering = ['stock_name']