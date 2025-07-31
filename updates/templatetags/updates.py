from django import template 
from django.shortcuts import reverse

from..models import Post, Comment

register = template.Library()

@register.simple_tag
def only_comments(post):
    """Return only comments of a post"""
    
    comments = post.only_comments()
    return comments
 
@register.simple_tag
def resolve_url(reply):
    """Get the appropriate url to go back """
    
    parent_reply = reply.reply
    if parent_reply:
        return reverse("updates:show_replies_of_a_reply", args=[parent_reply.id])
    else:
        return reverse("updates:comment_replies", args=[reply.id])
    
@register.filter
def get_parent_reply(reply):
    """Return parent reply if not found return the reply """
    
    parent_reply = reply.reply
    if parent_reply :
        return parent_reply.id
    else:
        return reply.id