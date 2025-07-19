from django.db import models
from accounts.models import User

# Create your models here.

class Message(models.Model):
    """A class representing the messages model"""
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    text = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        ordering = ["-timestamp"]
    
    def __str__(self):
        """A string representation of the model """
        
        return f"Message {self.timestamp}"
        
        
class Chat(models.Model):
    """A class representation of an individual chat"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    friend =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    message =  models.ForeignKey(Message, on_delete=models.CASCADE, related_name="messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["timestamp"]
        
    def __str__(self):
        """String representation of chat"""
        
        return f"{self.user}-{self.friend}"