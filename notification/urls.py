from django.urls import path 

from.views import Home, Chats, SearchChats, Compose, AreYouSure, Delete 

app_name = "notification"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("chats/<str:username>/", Chats.as_view(), name="chats"),
    path("search/<str:text>/", SearchChats. as_view(), name="chat_search"),
    path("compose/<str:username>/",  Compose.as_view(), name="compose"),
    path("delete/<int:id>/<str:friend>/", AreYouSure. as_view(), name="delete_message"), 
    path("delete-done/<int:id>/<str:friend>/", Delete.as_view(), name="delete_done")
]