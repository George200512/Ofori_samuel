from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta 

from.models import Post

@receiver(post_save, sender=Post)
def set_expiry_date(sender, instance,  created, **kwargs):
    """Set the expiry date of a post instance"""
    
    if created and not instance.expires_on:
        post = Post.objects.get(id=instance.id)
        post.expires_on = post.created_at + timedelta(hours=24)
        post.save()