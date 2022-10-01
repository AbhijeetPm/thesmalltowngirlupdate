from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    bio = models.TextField()
    contect = models.CharField(max_length=10)
    fblink = models.URLField(max_length=200)
    twlink = models.URLField(max_length=200)
    gmlink = models.URLField(max_length=200)
    inlink = models.URLField(max_length=200)
    profile_img = models.ImageField(upload_to="profile_image")
    
    def __str__(self) -> str:
        return self.user

class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=200)
    main_content = models.TextField()
    b_image = models.ImageField(upload_to="blog_img")
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.blog_title

# class main_comment(models.Model):
#     comment = models.TextField()
#     date_time = models.DateTimeField(auto_now_add=True)
#     user_id = models.IntegerField(default=None)
#     blog_id = models.IntegerField(default=None)



# class replyid_comment(models.Model):
#     comment  = models.TextField()
#     date_time = models.DateTimeField(auto_now_add=True)
#     user_id = models.IntegerField(default=None)
#     blog_id = models.IntegerField(default=None)
#     main_comment = models.IntegerField(default=None)