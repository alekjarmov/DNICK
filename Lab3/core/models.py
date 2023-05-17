from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PostUser(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(PostUser, on_delete=models.CASCADE)
    content = models.TextField()
    files = models.FileField(upload_to='files/', blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(PostUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
