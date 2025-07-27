from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    """A class to manage user account creation."""
    
    def create_user(self, user_name, password, email, **kwargs):
        """Add a new active user"""
        
        if not user_name:
            raise ValueError ("Username must be present")
        elif not password:
            raise ValueError("Password must be present")
        elif not email:
            raise ValueError("Email must be present ")
        else:
            user = self.model(user_name=user_name,  email=self.normalize_email(email),  **kwargs)
            user.set_password(password)
            user.save(using=self._db)
            return user
            
    def create_superuser(self, user_name, password, email):
        """Creates a user that has extra permissions than a normal user"""
        
        user = self.create_user(user_name=user_name, password=password, email=email)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
   
class User(AbstractBaseUser,  PermissionsMixin):
    """A class representing a user """
    
    email = models.EmailField("Email", unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    #profile_pic = models.ImageField(upload_to="images/user_pics", null=True,  blank=True)
=======
    profile_pic = models.ImageField(upload_to="images/user_pics", null=True,  blank=True)
>>>>>>> e48fab8c5cf2e6a5d67df8b8e2fc3d8aa401390a
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "user_name"
    REQUIRED_FIELDS = [ "email"]
    
    def __str__(self):
          """A string representation of the user"""
          
          return f"{self.user_name}"
       
    def has_perm(self, perm, obj=None):
           """Checks user has perm"""
           
           return self.is_admin
       
    def has_module_perm(self, app_label):
           """Checks if user has perm for an app """
           
           return self.is_admin
      
    @property
    def is_staff(self):
          """Checks if user is staff"""
          
          return self.is_admin