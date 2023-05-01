from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.

class Pins(models.Model):
    Pin = CloudinaryField('image')
    Title = models.CharField(max_length=255,blank=True,null=True)
    Description = RichTextField(blank=True,null=True)
    created_by = models.CharField(max_length=255,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True,null=True, related_name='Pin_like')
    
    def __str__(self):
        return self.Title

    def number_of_likes(self):
        return self.likes.count()

class Profile(models.Model):
    name = models.CharField(max_length=255)
    profile_photo = CloudinaryField('image')

    def __str__(self):
        return self.name
    
class Comments(models.Model):
    Post = models.ForeignKey(Pins,on_delete=models.CASCADE)
    Comment = models.TextField(blank=True,null=True)
    comment_by = models.ForeignKey(User,on_delete=models.CASCADE)
    commented_on = models.DateTimeField(auto_now_add=True)