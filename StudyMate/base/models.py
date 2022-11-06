
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length = 200)
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    post_image=models.ImageField(upload_to='images',null=True,blank=True)
    # this is a many to many relationship to user
    participants=models.ManyToManyField(User,blank=True,related_name='participants')
    likes=models.ManyToManyField(User,related_name='room_likes')
    updated = models.DateTimeField(auto_now = True) #auto_now takes snapshot on everytime we save the item  
    created = models.DateTimeField(auto_now_add=True) #auto_now_add only takes timestamp when we first saved the item

    class Meta:
        ordering = ['-updated' ,'-created']

    def __str__(self):
        return self.name

    def number_of_likes(self):
        return self.likes.count()



class Message(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE )
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    body =models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add =True)

    def __str__(self):
        return self.body[0:50]

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='images',null=True,default='default.jpg')
    bio=models.TextField(blank=True)
    follower=models.ManyToManyField(User,related_name='follower')

    def __str__(self):
        return f'{self.user.username} Profile'



