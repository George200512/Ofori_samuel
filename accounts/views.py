from django.shortcuts import render, redirect 
from django.views import View
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.urls import reverse_lazy
import re

from.forms import SignUpForm,  ProfileForm, ChangePasswordForm, LoginForm, ForgotPasswordForm, FindMyAccountForm
from .models import User 

# Create your views here.

class SignUp(View):
    """A class representing the signup view"""
    
    form_class = SignUpForm
    template_name = "accounts/html/signup.html"
    
    def get(self, request):
        """A Get method to handle get requests"""
        
        return render(request, self.template_name, {"form":self.form_class})
        
    def post(self, request):
        """A post method to handle post requests"""
        
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect("accounts:profile", username=user.user_name)
        return render(request, "accounts/html/signup.html", {"form":user_form})


class Profile(LoginRequiredMixin, View):
     """ A class representation of thee profile view"""
     
     profile_form = ProfileForm
     profile_template_name = "accounts/html/profile.html"
     
     def get(self, request, username):
         """A method that handles get requests"""
         
         user = User.objects.filter(user_name=username).first()
         if user:
             form = self.profile_form(instance=user)
             return render(request, self.profile_template_name, {"form":form, "username":username, "user":user})
         return redirect("accounts:signup")
   
          
     def post(self, request, username):
        """A method that handles post requests """
        
        user = User.objects.get(user_name=username)
        form = self.profile_form(data=request.POST, instance=user)
        if form.is_valid():
           user = form.save(commit=False)
           username = user.user_name
           user.save()
           return redirect("accounts:profile", username=username)      
        return render(request, self.profile_template_name, {"form": form,  "username":username})
        
        
class ChangePassword(LoginRequiredMixin, View):
    """A view for changing authenticated user password"""
    
    change_password_form = ChangePasswordForm
    template_name = "accounts/html/change-password.html"
    
    def get(self, request, username):
        """A Get method responsible for handling the get requests"""
        
        user = User.objects.get(user_name=username)
        form = self.change_password_form(user=user)
        return render(request, self.template_name, {"form":form, "username":username})
        
    def post(self, request, username):
        """A post method for handling post requests"""
        
        user = User.objects.get(user_name=username)
        form = self.change_password_form(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("accounts:profile", username=username)
        return render(request, self.template_name, {"form":form, "username":username})
        

class Logout(LoginRequiredMixin, View):
    """A logout view"""
    
    def get(self, request):
        """A Get method responsible for handling the get requests"""
        
        logout(request)
        return redirect("accounts:login")
        
        
class Login(View):
   """A login view class"""
   
   login_form = LoginForm
   template_name = "accounts/html/login.html"
    
   def get(self, request):
        """A Get method responsible for handling the get requests """
        
        form = self.login_form()
        return render(request, self.template_name, {"form":form})
        
   def post(self, request):
        """A post method to handle post requests"""
        
        form = self.login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, user_name=username, password=password)
            if user:
               login(request, user)
               return redirect("accounts:profile", username=user.user_name)
            return redirect("accounts:signup")
        return render(request, self.template_name, {"form":form})
        

class ForgotPassword(PasswordResetView):
    """A class representing the forgot password view"""
    
    template_name = "accounts/html/forgot-password.html"
    form_class = ForgotPasswordForm
    email_template_name = "accounts/html/email-reset-password.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    
    def get(self, request):
        """A Get method to handle get requests"""
        
        form = self.form_class()
        return  render(request, self.template_name, {"form":form})
        
        
class PasswordResetConfirm(PasswordResetConfirmView):
    """A class that acts similar to ChangePasswordView"""
    
    template_name = "accounts/html/change-password.html"
    post_reset_login = True 
    form_class = ChangePasswordForm
    
    
class PasswordResetDone(PasswordResetDoneView):
    """A class representing the password reset done view"""
    
    template_name = "accounts/html/password-reset-done.html"


class FindMyAccount(View):
    """A class responsible for handling find-my-account requests"""
    
    template_name = "accounts/html/find-my-account.html"
    form_class = FindMyAccountForm
    
    def get(self, request):
        """A Get method responsible for handling the get requests"""
        
        form = self.form_class()
        return render(request, self.template_name, {"form":form})
        
    def is_email(self, string):
        """Checks if string is a valid email"""
        
        regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,}$"
        pattern = re.compile(regex)
        if pattern.fullmatch(string):
            return True 
        return False 
        
    def post(self, request):
        """A post method to handle post requests"""
        
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_username"]
            if self.is_email(data):
                emails = User.objects.values_list("email", flat=True)
                if data in emails:
                    user = User.objects.get(email=data)
                    return redirect("accounts:user_found", username=user.user_name)                
                else:
                    return render(request, self.template_name, {"form":form})
            else:
                usernames = User.objects.values_list("user_name", flat=True)
                if data in usernames:
                    user = User.objects.get(user_name=data)
                    return redirect("accounts:user_found", user.user_name)
                else:
                    return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})
        
        
class UserFound(View):
   """A view rendered when a user is found"""
   
   template_name = "accounts/html/user-found.html"
   
   def get(self, request, username):
       """A page rendered when a user is found."""
       
       return render(request, self.template_name, {"username":username})
   