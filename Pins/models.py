from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from random import randint
# Create your models here.

class Pins(models.Model):
    Pin = CloudinaryField('image')
    Title = models.CharField(max_length=255,blank=True,null=True)
    Description = RichTextField(blank=True,null=True)
    created_by = models.CharField(max_length=255,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Title

class Profile(models.Model):
    name = models.CharField(max_length=255)
    profile_photo = CloudinaryField('image')

    def __str__(self):
        return self.name