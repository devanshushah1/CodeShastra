from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    country = models.CharField(max_length=100, default='India', null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    email_verified_hash = models.CharField(max_length=255, null=True, blank=True)
    email_verified = models.IntegerField(default=0, null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Keywords(models.Model):
    name = models.CharField(max_length=200 , null=True)
    def __str__(self):
       return self.name

class Item(models.Model):
    brand_name = models.CharField(max_length=100, null=True, blank=True)
    keyword = models.ManyToManyField(Keywords)
    is_found = models.BooleanField(default=True)
    is_claimed = models.BooleanField(default=True)
    posted_by = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    Image = models.ImageField(null=True, blank=True)
    date_posted = models.DateField(auto_now_add=True)
    def __str__(self):
       return self.brand_name

class Claims(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    def __str__(self):
       return self.item

