from django import template 

from..models import Post 

register = template.Library()

@register.simple_tag
def only_comments(post):
    comments = post.only_comments()
    return comments
    