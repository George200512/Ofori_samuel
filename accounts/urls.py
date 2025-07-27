from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 

from.views import SignUp, Profile,  ChangePassword, Logout, Login, ForgotPassword, PasswordResetConfirm, PasswordResetDone, FindMyAccount, UserFound

app_name = "accounts"

urlpatterns = [
    path("signup", SignUp.as_view(), name="signup"),
    path("profile/<str:username>/", Profile.as_view(), name="profile"),
    path("profile/<str:username>/change-password", ChangePassword. as_view(), name="change_password"),
    path("logout", Logout.as_view(), name="logout"),
    path("login", Login.as_view(), name="login"),
    path("forgot-password/", ForgotPassword. as_view(), name="forgot_password"),
    path("password-reset-confirm/<uidb64>/<token>", PasswordResetConfirm. as_view(), name="password_reset_confirm"),
    path("password-reset-done",  PasswordResetDone.as_view(), name="password_reset_done"),
    path("find-my-account", FindMyAccount.as_view(), name="find_my_account"),
    path("user-found/<str:username>", UserFound. as_view(), name="user_found")
]

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)