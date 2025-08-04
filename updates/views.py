from django.shortcuts import render, redirect 
from django.views import View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Now
from django.views.generic import FormView, ListView, TemplateView

from accounts.models import User 
from.models import Comment, Post, Viewer
from .forms import MakePostForm, CommentForm

# Create your views here.

class Home(LoginRequiredMixin,  View):
    """A home View for displaying your updates and other users update."""
    
    template_name = "updates/html/index.html"
    
    def get(self, request):
        """A method that handles get requests """
        
        other_updates = User.objects.filter(Q(posts__expired=False) & ~Q(posts__user=request.user)).distinct()
        expired_posts = Post.objects.filter(expires_on__lt=Now(), expired=False)
        if expired_posts.exists():
            expired_posts.update(expired=True)
        return render(request, self.template_name, { "user":request.user, "other_updates":other_updates})
        
        
class PersonalUpdates(LoginRequiredMixin,  View):
    """A view responsible for rendering personal updates"""
    
    template_name = "updates/html/personal-updates.html"
    
    def get(self, request):
        """A method that handles get requests"""
        
        return render(request, self.template_name, {"user":request.user})
        
        
class Comments(LoginRequiredMixin, View):
    """A view responsible for displaying the comments of a posts"""
    
    template_name = "updates/html/comment.html"
    
    def get(self, request, id):
        """A method that handles get requests """
        
        post = Post.objects.get(id=id)
        return render(request, self.template_name, {"post":post, "user":request.user})
        
        
class Viewers(LoginRequiredMixin, View):
    """A view class responsible for displaying the viewers"""
    
    template_name = "updates/html/viewer.html"
    
    def get(self, request, id):
        """A method that handles handles get requests"""
        
        post = Post.objects.get(id=id)
        return render(request, self.template_name, {"post":post, "user":request.user})
        
        
class MakePost(LoginRequiredMixin, View):
    """A view responsible for making a post """
    
    template_name = "updates/html/make-post.html"
    form_class = MakePostForm 
    
    def get(self, request):
        """A method that handles get requests """
        
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "user":request.user})
        
    def post(self, request):
        """A method that handles post requests """
        
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            request.user.posts.add(post)
            return redirect("updates:your_updates")
        return render(request, self.template_name, {"form": form, "user":user})
        
        
class AreYouSure(LoginRequiredMixin, View):
    """A view responsible for Deleting a post"""
    
    template_name = "updates/html/are-u-sure.html"
    
    def get(self, request, id):
        """A method that handles get requests """
        
        post = Post.objects.get(id=id)
        return render(request, self.template_name, {"post": post, "user":request.user})

        
class DeletePost(LoginRequiredMixin, View):
    """A view responsible for Deleting a post"""
    
    template_name = "updates/html/success.html"
    
    def get(self, request, id):
        """A method that handles get requests """
        
        post = Post.objects.get(id=id)
        post.delete()
        return render(request, self.template_name,  {"user":request.user})
                                                
        
class DisplayUpdates(LoginRequiredMixin, View):
    """A class responsible for displaying a User's update"""
    
    template_name = "updates/html/display.html"
    
    def get(self, request, username):
        """A method that handles get requests """
        
        user = User.objects.get(user_name=username)
        valid_posts = Post.objects.filter(user=user, expired=False)
        for post in valid_posts:
            Viewer.objects.get_or_create(user=request.user, post=post)
        return render(request, self.template_name, {"valid_posts":valid_posts,  "user":request.user})
        
        
class EditPost(LoginRequiredMixin, View):
    """A view for editing posts"""
    
    template_name = "updates/html/edit-post.html"
    form_class = MakePostForm 
    
    def get(self, request, id):
        """A method that handles get requests """
        
        post = Post.objects.get(id=id)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {"form":form,  "post":post,  "user":request.user})
        
    def post(self, request, id):
        """Save the edited post to database"""
        
        post =Post.objects.get(id=id)
        form = self.form_class(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect("updates:your_updates")
        return render(request, self.template_name, {"form":form, "post":post,  "user":request.user})
        
        
class PostComment(LoginRequiredMixin, View):
    """A view for posting a comment"""
    
    template_name = "updates/html/post-comment.html"
    form_class = CommentForm
    
    def get(self, request, id):
        """Display comment form"""
        
        form = self.form_class()
        post = Post.objects.get(id=id)
        return render(request, self.template_name, {"form":form,  "post":post,  "user":request.user})
        
    def post(self, request, id):
        """Save comment to database"""
        
        form = self.form_class(request.POST)
        post = Post.objects.get(id=id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.from_user = request.user
            comment.to_user = post.user
            comment.post = post 
            comment.save()
            post.comments.add(comment)
            return redirect("updates:comments", id=id)
        return render(request, self.template_name, {"form":form,  "post":post,  "user":request.user})
        
        
class Reply(LoginRequiredMixin, View):
    """A view that handles a comment's reply"""
    
    template_name = "updates/html/post-reply.html"
    form_class = CommentForm
    
    def get(self, request, id):
        """Display comment form"""
        
        form = self.form_class()
        comment = Comment.objects.get(id=id)
        return render(request, self.template_name, {"form":form,  "comment":comment,  "user":request.user})
        
    def post(self, request, id):
        """Save reply in database """
        
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(id=id)
            reply = form.save(commit=False)
            reply.is_reply = True
            reply.from_user = request.user
            reply.to_user = comment.from_user
            reply.post = comment.post
            reply.save()
            comment.replies.add(reply)
            return redirect("updates:comment_replies", id=id)
        else:
            comment = Comment.objects.get(id=id)
            return render(request, self.template_name, {"form":form,  "comment":comment,  "user":request.user})
            
            
class ShowCommentReplies(LoginRequiredMixin, View):
    """A view  that displays the replies of a comment"""
    
    template_name = "updates/html/show-replies.html"
   
    def get(self, request, id):
       """Get the comment with specified id and display the replies"""
       
       comment = Comment.objects.get(id=id)
       return render(request, self.template_name, {"comment":comment, "user":request.user})
       
       
class PostReplyReply(LoginRequiredMixin, FormView):
    """Compose and reply to the reply of a reply"""
    
    form_class = CommentForm  
    template_name = "updates/html/compose-replys-reply.html"
    
    def form_valid(self, form):
        """Add the reply of the reply to the database"""
        
        reply = form.save(commit=False)
        id = self.kwargs["id"]
        parent_reply = Comment.objects.get(id=id, is_reply=True)
        reply.is_reply = True 
        reply.from_user = self.request.user
        reply.to_user = parent_reply.from_user 
        reply.post  = parent_reply.post
        reply.save()
        parent_reply.replies.add(reply)
        return redirect("updates:show_replies_of_a_reply", id=id)
     
    def dispatch(self, request, *args, **kwargs):
        """A method to determine which http method the request 
        will get dispatched to"""
        
        reply = Comment.objects.get(id=kwargs["id"])
        self.parent_reply = reply.reply 
        return super().dispatch(request, *args, **kwargs)
        
          
    def get_context_data(self, **kwargs):
        """Add extra data to the template"""
        
        context = super().get_context_data(**kwargs)
        context["p_reply"] = self.parent_reply
        return context
        
        
class ShowRepliesOfAReply(LoginRequiredMixin, ListView):
    """Show the replies of a reply"""
    
    model = Comment
    template_name = "updates/html/show-replies-of-a-reply.html"
    context_object_name = "replies"
    
    def get_queryset(self):
        """Get the replies of a reply"""
        
        id = self.kwargs["id"]
        reply = Comment.objects.get(id=id)
        return reply.replies.all()
        
    def get_context_data(self, **kwargs):
        """Add the reply that the reply is replying to"""
        
        reply = Comment.objects.get(id=self.kwargs["id"])
        context = super().get_context_data(**kwargs)
        context["reply"] = reply 
        return context
        
  
class EditComment(LoginRequiredMixin,  View):
    """A view that allows you to edit a comment"""
    
    model = Comment 
    template_name = "updates/html/comment-settings/edit-comment.html"
    form_class = CommentForm 
    
    def get(self, request, id):
        """Display the form to the user"""
        
        comment = Comment.objects.get(id=id)
        form = self.form_class(instance=comment)
        return render(request, self.template_name, {"user":request.user, "form":form,  "comment":comment})
        
    def post(self, request, id):
        """Save the form to the database """
        
        comment = Comment.objects.get(id=id)
        form = self.form_class(instance=comment, data=request.POST)
        if form.is_valid():
            edited_comment = form.save()
            return redirect("updates:comments",  id=edited_comment.post.id)
        return render(request, self.template_name, {"user": request.user, "form": form, "comment":comment})
        
 
class AreYouSureYouWantToDeleteComment(LoginRequiredMixin, View):
    """A view that displays an html webppage asking if you want to
    delete the comment"""
    
    template_name = "updates/html/comment-settings/are-you-sure-you-want-to-delete-comment.html"
    
    def get(self, request, id):
        """A method that displays the webpage"""
        
        comment = Comment.objects.get(id=id)
        return render(request,  self.template_name,  {"user": request.user,  "comment":comment})
        
      
class DeleteComment(LoginRequiredMixin, View):
    """Delete a comment """
    
    def get(self, request, id):
        """A method to delete the comment"""
        
        post = Comment.objects.get(id=id).post
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect("updates:comments", id=post.id)
        
       
class CommentSettings(LoginRequiredMixin, TemplateView):
    """A view that displays the settings of a comment"""
    
    template_name = "updates/html/comment-settings/comment-settings.html"
    
    def get_context_data(self, **kwargs):
        """Get the id of the comment"""
        
        id = self.kwargs["id"]
        comment = Comment.objects.get(id=id)
        context = super().get_context_data(**kwargs)
        context["comment"] = comment 
        return context 