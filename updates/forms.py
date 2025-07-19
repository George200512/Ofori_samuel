from django import forms 

from .models import Post, Comment

class MakePostForm(forms.ModelForm):
    """A form for making post"""
    
    class Meta :
        model = Post
        fields = ["description", "content"]
        widgets = {
            "description":forms.TextInput(attrs={"class":"description", "placeholder":"Description"}),
            "content":forms.Textarea(attrs={"class":"content", "placeholder":"Write something..."})
        }
        

class CommentForm(forms.ModelForm):
    """A for writing comments"""
    
    class Meta:
         model = Comment
         fields = ["text"]
         widgets = {
             "text":forms.TextInput(attrs={"class":"text-comment", "placeholder":"Leave a comment"})
         }
                 