from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    dados = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    