from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BlogUser(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog")
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        # return max 20 letters
        return self.content[:20] + "..." if len(self.content) > 20 else self.content


class BlockList(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name="blocker_user")
    blocked_user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, related_name='blocked_users')

    def __str__(self):
        return self.user.user.username + " blocked " + self.blocked_user.user.username


class File(models.Model):
    file = models.FileField(upload_to='files/', blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_file")

    def __str__(self):
        return "File for " + self.blog.title + " blog"
