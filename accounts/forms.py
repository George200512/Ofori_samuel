from django import forms 
from django.forms import ModelForm, Form
import re
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm

from .models import User
               
class SignUpForm(ModelForm):
        class Meta:
            model = User
            fields = ["user_name",  "email", "password"]
            widgets = {
                "email":forms.EmailInput(attrs={"class":"email"}),
                "password":forms.PasswordInput(attrs={"class":"password"}),
                "user_name":forms.TextInput(attrs={"class":"user_name", "pattern":"^[a-zA-Z0-9_]{8,}$"}),
            }
        confirm_password = forms.CharField(help_text="Confirm Password", widget=forms.PasswordInput(attrs={"class":"password"}))
        symbols = ["#", '@', "$", "/", "\\", "<", ">", "."]
    
        def clean_email(self):
            """Check email"""
        
            return self.cleaned_data["email"]
        
        def clean_password(self):
            """Check password """
            
            symbols = "".join(self.symbols)
            escape_symbols = re.escape("".join(self.symbols))
            regex = f"^[a-zA-Z0-9{escape_symbols}]{{8,}}$"
            pattern = re.compile(regex)
            password = self.cleaned_data["password"]
            
            if pattern.fullmatch(password):
                return password 
            else:
                if len(password) < 8:
                    raise forms.ValidationError("Password should be at least eight characters long. ")
                elif not any(char in password for char in self.symbols):
                    raise forms.ValidationError(f"Password must contain atleast one of these special characters:{','.join(self.symbols)}")
                else:
                    raise forms.ValidationError("Password does not match the pattern.    ")
        
        def clean_user_name(self):
            """Check user name"""
            
            regex = "^[a-zA-Z0-9_]{8}+"
            pattern = re.compile(regex)
            username = self.cleaned_data["user_name"]
            if pattern.search(username):
                return username
            else:
                raise forms.ValidationError("User name must start with a an alphanumeric character.\n The only valid character is underscore. \nAtleast eight characters long")
            
        def clean_confirm_password(self):
               """Confirm Password """
               
               confirm_password = self.cleaned_data["confirm_password"]
               password = self.cleaned_data.get("password")
               
               if password == confirm_password :
                   return confirm_password 
               else:
                   raise forms.ValidationError("Password mismatch")
               
        def clean(self):
               """Strip all cleaned data"""
               
               cleaned_data =  super().clean()
               password = cleaned_data.get("password")
               password = make_password(password)
               cleaned_data["password"] = password
                       
               for data in cleaned_data :
                   cleaned_data[data] = cleaned_data[data].strip()
               return cleaned_data
               
                       
class ProfileForm(SignUpForm):
       class Meta:
           model = User
           fields = ["user_name", "email"]
       confirm_password = forms.CharField(help_text="Confirm Password", widget=forms.PasswordInput(attrs={"class":"password"}), required=False)
               
       def clean_password(self):
           pass
               
       def clean_confirm_password(self):
               pass
               
       def clean(self):
               """Validate all of users input """
               
               cleaned_data = ModelForm.clean(self)
               for data in cleaned_data :
                   if cleaned_data[data]:
                       cleaned_data[data] = cleaned_data[data].strip()
               return cleaned_data
               
               
class ChangePasswordForm(SetPasswordForm):
    """A form that handles the user changed and setting it."""
    
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"new-password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"confirm-password"}))
    symbols = ["#", '@', "$", "/", "\\", "<", ">", "."]
    
    def save(self, commit=True):
        """Save form to database """
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit :
            user.save()
        return user
        
    def clean_new_password(self):
        """Validate password"""
        
        symbols = "".join(self.symbols)
        escape_symbols = re.escape("".join(self.symbols))
        regex = f"^[a-zA-Z0-9{escape_symbols}]{{8,}}$"
        pattern = re.compile(regex)
        password = self.cleaned_data["new_password"]
        
        if pattern.fullmatch(password):
            if check_password(password, self.user.password):
                raise forms.ValidationError("Password must be different from the previous.")
            return password 
        else:
            if len(password) < 8:
                raise forms.ValidationError("Password should be at least eight characters long. ")
            elif not any(char in password for char in self.symbols):
                raise forms.ValidationError(f"Password must contain atleast one of these special characters:{','.join(self.symbols)}")
            else:
                raise forms.ValidationError("Password does not match the pattern.")
                
    def clean_confirm_password(self):
        """Check confirmation password """
        
        password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        
        if password and password == confirm_password :
            return confirm_password 
        else:
            raise forms.ValidationError("Password mismatch.")
            
    def clean(self):
        """Make a hash password"""
        
        cleaned_data = super().clean()
        cleaned_data["new_password"] = make_password(cleaned_data["new_password"])
        return cleaned_data 


class LoginForm(Form):
    """A login form class"""
    
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"username",  "placeholder":"Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"password",  "placeholder":"Password"}))
    symbols = ["#", '@', "$", "/", "\\", "<", ">", "."]
    
    def clean_username(self):
        """Check username """
        
        regex = "^[a-zA-Z0-9_]{8,}"
        pattern = re.compile(regex)
        cleaned_data = super().clean()
        username = cleaned_data["username"]
        if pattern.search(username):
            if User.objects.filter(user_name=username).first():
                return username
            raise forms.ValidationError("Username not found. ")            
        else:
            raise forms.ValidationError("User name must start with a an alphanumeric character.\n The only valid character is underscore. \nAtleast eight characters long")
            
    def clean_password(self):
        """Validate password"""
        
        symbols = "".join(self.symbols)
        escape_symbols = re.escape("".join(self.symbols))
        regex = fr"^[a-zA-Z0-9{escape_symbols}]{{8,}}$"
        pattern = re.compile(regex)
        password = self.cleaned_data["password"]
        
        if pattern.fullmatch(password):
            return password 
        else:
            if len(password) < 8:
                raise forms.ValidationError("Password should be at least eight characters long. ")
            elif not any(char in password for char in self.symbols):
                raise forms.ValidationError(f"Password must contain atleast one of these special characters:{','.join(self.symbols)}")
            else:
                raise forms.ValidationError("Password does not match the pattern.")
                
    def clean(self):
        """Validate all user input"""
        
        self.cleaned_data["password"] = self.cleaned_data["password"].strip()
        password = self.cleaned_data["password"]
        username = self.cleaned_data["username"]
        user = User.objects.filter(user_name=username).first()
        if not check_password(password, user.password):
            raise forms.ValidationError("Invalid password entered.")
        return cleaned_data 
        

class ForgotPasswordForm(PasswordResetForm):
    """A form to handle resetting forgotting passwords """
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"email"}))
    

class FindMyAccountForm(Form):
    """A form that handles the find-my-account form"""
    
    email_username = forms.CharField(widget=forms.TextInput(attrs={"class":"email-username", "placeholder":"Email or Username"}))
    
    def is_email(self, string):
        """Checks if string is a valid email"""
        
        regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,}$"
        pattern = re.compile(regex)
        if pattern.fullmatch(string):
            return True 
        return False
        
    def clean_email_username(self):
        """Checks input"""
        
        data = self.cleaned_data["email_username"].strip()
        if self.is_email(data):
            emails = User.objects.values_list("email", flat=True)
            if data in emails :
                return data
            return forms.ValidationError("Email not found.")
        else:
            user_names = User.objects.values_list("user_name", flat=True)
            if data in user_names:
                return data
            raise forms.ValidationError("Username not found. ")
    