from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
    class meta:
        ordering = ['order']

class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    image = models.URLField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likedposts', through='LikedPost')
    tags = models.ManyToManyField(Tag, related_name="posts")
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"liked by {self.user.username}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        try: 
            return  f"Comment by {self.author.username} on {self.created} "
        except:
            return f"no author on {self.created}"

class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'
            
        
        
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    class Meta:
        ordering = ['created']
        
class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'
    
    