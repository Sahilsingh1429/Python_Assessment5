from django.db import models

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name= models.CharField(max_length=50)
    username=models.CharField(max_length=100)
    email =models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name
    
    
class Insurance(models.Model):
    c1 = [ ('Health Insurance', 'Health Insurance'),
                  ('Life Insurance', 'Life Insurance'),
                   ('Car Insurances', 'Car Insurances'),
                    ]
    insurance_name = models.CharField(max_length=100)
    insurance_duration =models.IntegerField()
    insurance_premium =models.FloatField()
    insurance_category = models.CharField(max_length=100, choices=c1)

    def __str__(self):
        return self.insurance_name
    
class Purchases(models.Model):
    insurance_i =models.ForeignKey(Insurance,on_delete=models.CASCADE)
    user_i=models.ForeignKey(User,on_delete=models.CASCADE)