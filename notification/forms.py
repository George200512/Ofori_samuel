from django import forms
import re

from accounts.models import User 
from .models import Message 


class SearchForAFriendForm(forms.Form):
    """A form that displays a text input for searching for friends"""
    
    text = forms.CharField(widget=forms.TextInput(attrs={"class":"search-field", "placeholder":"Search for a friend by name or email"}))
    
    def clean_text(self):
        """Validate text field"""
        
        data = self.cleaned_data["text"].strip()
        is_email = self.is_email(data)
        if is_email :
            if User.objects.filter(email=data):
                return data
            self.add_error("text", "User With Email Not Found.")
        else: 
            if User.objects.filter(user_name=data):
                return data
            self.add_error("text", "User With Username Not Found")
        
    def is_email(self, string):
        """Checks if string is a valid email"""
        
        regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,}$"
        pattern = re.compile(regex)
        if pattern.fullmatch(string):
            return True 
        return False 
        
        
class ComposeForm(forms.ModelForm):
    """A form class for composing messages"""
    
    class Meta:
        model = Message
        fields = ["text"]
        widgets = {
            "text":forms.Textarea(attrs={"class":"message-text", "placeholder":"Compose your message."})
        }