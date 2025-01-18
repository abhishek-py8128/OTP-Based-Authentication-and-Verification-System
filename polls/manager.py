from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager): # BaseUserManager provide methods to manage user creation.
    use_in_migrations = True # This attribute allows the manager to be used during migrations.
    
    def _create_user(self, email, password, **extra_fields): # creating both regular and super users .
        """
        Creates and saves a user with the given email and password.
        """
        if not email:
            raise ValueError(_('The given email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # use self._db instead of self.db
        return user

    def create_user(self, email, password=None, **extra_fields): # creating a regular user .
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user         
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)
    
    
# ===== Set the custom user model in your settings.py with AUTH_USER_MODEL. =====