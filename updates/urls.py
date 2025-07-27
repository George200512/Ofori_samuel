from django.urls import path 

from.views import (
    Home, PersonalUpdates, Comments, Viewers,  MakePost,
    AreYouSure, DeletePost, DisplayUpdates, EditPost ,
    PostComment, Reply,  ShowCommentReplies,
    PostReplyReply 
    )

app_name = "updates"

urlpatterns = [
    path("",  Home.as_view(), name="home"),
    path("your-updates/", PersonalUpdates. as_view(), name="your_updates"),
    path("comments/<int:id>/", Comments.as_view(), name="comments"),
    path("viewers/<int:id>/", Viewers .as_view(), name="viewers"), 
    path("post", MakePost. as_view(), name="post"),
    path("post/<int:id>/are-you-sure", AreYouSure.as_view(), name="are_you_sure"),
    path("delete-success/<int:id>", DeletePost.as_view(), name="delete_success"),
    path("display-updates/<str:username>/", DisplayUpdates. as_view(), name="display_updates"),
    path("post/delete/<int:id>/",  EditPost. as_view(), name="edit_post"), 
    path("post-comment/<int:id>", PostComment. as_view(), name="post_comment"),
    path("post-comment-reply/<int:id>", Reply. as_view(), name="post_reply"),
    path("comment-reply-show/<int:id>", ShowCommentReplies. as_view(), name="comment_replies"), 
    path("reply/<int:id>/reply-compose/",  PostReplyReply. as_view(), name="compose_replys_reply")
]