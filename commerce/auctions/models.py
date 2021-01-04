from django.contrib.auth.models import AbstractUser
from django.db import models

import datetime
from django.utils import timezone

class User(AbstractUser):
    pass


class Post (models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE ,related_name="userid")
    title = models.CharField(max_length=50)
    description = models.TextField(default='')
    category = models.CharField(max_length=64)
    img = models.ImageField(upload_to='post_img',null=True ,blank=True)
    created = models.DateTimeField(default=datetime.datetime.now())
    active = models.BooleanField(default=True)
    seller = models.CharField(max_length=50)
    starting_bid = models.IntegerField()
    def __str__(self):
        return f"{self.title}&{self.description}"



class comment (models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE )
    post_id = models.ForeignKey(Post , on_delete=models.CASCADE )
    comment = models.TextField(default='')
    created = models.DateTimeField(default=datetime.datetime.now())



class bid (models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE )
    post_id = models.ForeignKey(Post , on_delete=models.CASCADE )
    bid = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return f"{self.bid}"

class Watchlist(models.Model):
    user_id = models.ForeignKey(User , on_delete=models.CASCADE )
    post_id = models.ForeignKey(Post , on_delete=models.CASCADE )