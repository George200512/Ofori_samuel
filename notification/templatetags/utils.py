from django import template 
from django.db.models import Q 

from notification.models import Chat, Message
from accounts.models import User 

register = template.Library()

@register.filter
def no_unread_messages(user, friend):
    """Get number of unread messages"""
    
    temp1 = Q(from_user=friend, to_user=user, read=False)
    my_unread_messages = Message.objects.filter(temp1)
    no_unread_messages = my_unread_messages.count()
    if no_unread_messages > 99:
        return f"99+"
    elif no_unread_messages == 0:
        return ""
    return no_unread_messages 
    
@register.simple_tag
def latest_message(user, friend):
    """Return shorten text if the length of the text is greater than 25"""
    
    temp = Q(from_user=user, to_user=friend)
    temp2 = Q(from_user=friend, to_user=user)
    my_chats = Message.objects.filter(temp | temp2).filter()
    if my_chats :
        latest = my_chats[0].text
        if len(latest) > 25:
            return f"{latest[0:24]}..."
        return latest
    return "No conversation started."
    
@register.simple_tag
def mark_as_read(message):
    message.read = True 
    message.save()
    return ""