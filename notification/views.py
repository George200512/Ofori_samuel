from django.shortcuts import render, redirect 
from django.views import View
from django.contrib.auth import login, logout 
from django.http import HttpResponse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import re
from django.utils import timezone 

#from accounts.forms import LoginForm
from accounts.models import User 
from . models import Message, Chat
from.forms import SearchForAFriendForm, ComposeForm 

# Create your views here.

class Home(LoginRequiredMixin, View):
    """The homepage for the notification app"""
    
    template_name = "notification/html/index.html"
    form_class = SearchForAFriendForm
    
    def get(self, request):
        """A Get method that handles get requests"""
        
        user = request.user
        temp = Q(friends__user=user)
        temp2 = Q(users__friend=user)
        my_friends = User.objects.filter(temp | temp2).distinct()
        form = self.form_class()
        return render(request, self.template_name, {"my_friends":my_friends, "form":form, "user":user})
        
    def post(self, request):
        """A method that handles post requests"""
        
        form = self.form_class(request.POST)
        user = request.user
        temp = Q(friends__user=user)
        temp2 = Q(users__friend=user)
        my_friends = User.objects.filter(temp | temp2).distinct()
        if form.is_valid():
            return redirect("notification:chat_search", text=form.cleaned_data["text"])
        return render(request, self.template_name, {"form":form, "my_friends":my_friends, "user":user})
        
        
class Chats(LoginRequiredMixin, View):
    """A view class responsible for displaying messages"""
    
    template_name = "notification/html/messages.html"
    
    def get(self, request, username):
        """A Get method responsible for handling the get requests"""
        
        my_chats = Chat.objects.filter(user=request.user,  friend__user_name=username)
        temp = Q(from_user__user_name=username, to_user=request.user, read=False)
        temp = Message.objects.filter(temp).filter()
        temp.update(read=True) 
        return render (request, self.template_name,  {"my_chats":my_chats, "user":request.user, "friend":username})
        
        
class SearchChats(LoginRequiredMixin, View):
    """A view responsible for rendering that result of a search"""
    
    template_name = "notification/html/searh-results.html"
    
    def get(self, request, text):
        """A method that handles get requests """
       
        is_email = self.is_email(text)
        if is_email :
            results = User.objects.filter(email__contains=text)
        else:
            results = User.objects.filter(user_name__contains=text)
        return render(request, self.template_name, {"results":results})
        
    def is_email(self, string):
        """Checks if string is a valid email"""
        
        regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9]{2,}$"
        pattern = re.compile(regex)
        if pattern.fullmatch(string):
            return True 
        return False

        
class Compose(LoginRequiredMixin, View):
    """A class view responsible for composing messages """
    
    template_name = "notification/html/compose.html"
    form_class = ComposeForm
    
    def get(self, request, username):
        """A Get method responsible for handling the get requests """
        
        form = self.form_class()
        return render(request, self.template_name, {"form":form,  "username":username})
        
    def post(self, request, username):
        """A method that handles post requests """
        
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.to_user = User.objects.get(user_name=username)
            message.timestamp = timezone.now()
            message.save()
            chat = Chat(user=request.user, friend=User.objects.get (user_name=username), message=message, timestamp=timezone.now())
            if User.objects.get(user_name=username) == request.user:
               chat.save()
            else:
               chat.save()
               chat2 = Chat(friend=request.user, user=User.objects.get (user_name=username), message=message, timestamp=timezone.now()) 
               chat2.save()
            return redirect("notification:chats", username=username)
        return render(request, self.template_name, {"form":form,  "username":username})  

                                   
class AreYouSure(LoginRequiredMixin, View):
    """A class based view for Deleting messages"""
    
    template_name = "notification/html/are-u-sure.html"
    
    def get(self, request, id, friend):
        """A method that handles get requests """
        
        message = Message.objects.filter(id=id).first()
        friend = User.objects.get(user_name=friend)
        return render(request, self.template_name, {"message":message, "friend":friend})
        
                      
class Delete(LoginRequiredMixin,  View):
    """A class based view for Deleting a messaage"""
    
    success_template_name = "notification/html/success.html"
    
    def get(self, request, id, friend):
       """A method that handles get requests """
       
       message = Message.objects.get(id=id)
       friend = User.objects.get(user_name=friend)
       message.delete()
       return render(request, self.success_template_name, {"friend": friend})
       