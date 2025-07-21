from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import identify_hasher, make_password
from django.utils import timezone
from polymorphic.models import PolymorphicModel



class CustomUserManager(BaseUserManager):
    USERNAME_REQUIRED = "The username field must be set"
    STAFF_REQUIRED = "Superuser must have is_staff as True"
    SUPERUSER_REQUIRED = "Superuser must have is_superuser as True"


    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(self.USERNAME_REQUIRED)
        user = self.model(username=user, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(self.STAFF_REQUIRED)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(self.SUPERUSER_REQUIRED)
        
        return self.create_user(username=username, password=password, **extra_fields)






class User(PolymorphicModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    objects = CustomUserManager()


    def save(self, *args, **kwargs):
        if self.password:
            try:
                identify_hasher(self.password)
            except ValueError:
                self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.username
    




class Customer(User):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='customers/', null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.username
    






class OTP(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=5)


    class Meta:
        indexes = [
            models.Index(fields=["customer", "created_at"])
        ]

    def mark_otp_expired(self):
        if not self.is_expired:
            self.is_expired = True
            self.expired_at = timezone.now()
            self.save(update_fields=["is_expired", "expired_at"])