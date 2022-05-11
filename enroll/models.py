from django.db import models

class User(models.Model):
    title= models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
   
    def __str__(self):
        return self.title