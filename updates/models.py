from django.db import models
from django.utils import timezone 
from datetime import timedelta 

from accounts.models import User 
from notification.models import Message 

# Create your models here.


class Post(models.Model):
    """A class representing a single post"""
    
    content = models.TextField(max_length=1200)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True) 
    expires_on = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    
    def __str__(self):
        """A string representation of the model  """
        
        return f"{self.description}"
        
    def only_comments(self):
        """Get only the comments of a post"""
        
        comments = self.comments.filter(is_reply=False)
        return comments


class Comment(Message):
    """A class representing the comment model"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name="comments")
    reply = models.ForeignKey("self", on_delete=models.CASCADE,  null=True,  blank=True,  related_name="replies")
    is_reply = models.BooleanField(default=False)
    
    def __str__(self):
        """A string representation of the model"""
        
        text = self.text
        if len(text) > 25:
            text = f"{text[0:24]}..."
        return f"{self.from_user}:{text}"
          
              
class Viewer(models.Model):
    """A module representing viewers of a post"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewed_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="viewers")
    viewed_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "post")         