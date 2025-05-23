from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
  AbstractBaseUser,
  BaseUserManager,
  PermissionsMixin,)

class UserManager(BaseUserManager):
  def create_user(self,email,password=None,**extra_fields):
    if not email:
      raise ValueError('user must enter the email')
    user=self.model(email=self.normalize_email(email),**extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self,email, password):
    user=self.create_user(email,password)
    user.is_staff=True
    user.is_superuser=True
    user.save(using=self._db)

    return user


class User(AbstractBaseUser,PermissionsMixin):
  email=models.EmailField(max_length=255,unique=True)
  name=models.CharField(max_length=255)
  is_active=models.BooleanField(default=True)
  is_staff=models.BooleanField(default=False)

  objects=UserManager()

  USERNAME_FIELD='email'

class Party(models.Model):
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  name=models.CharField(max_length=255)

  def __Str__(self):
    return self.name

  def total_given(self):
    return self.transactions.filter(transaction_type='given').aggregate(models.Sum('amount'))['amount__sum'] or 0

  def total_taken(self):
    return self.transactions.filter(transaction_type='taken').aggregate(models.Sum('amount'))['amount__sum'] or 0

class Transaction(models.Model):
  TRANSACTION_TYPE=(
    ('given','Given'),
    ('taken','Taken'),
  )
  user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
  party=models.ForeignKey(Party,on_delete=models.CASCADE,related_name='transactions')
  amount=models.DecimalField(max_digits=10,decimal_places=2)
  transaction_type=models.CharField(max_length=6,choices=TRANSACTION_TYPE)
  note=models.TextField(blank=True,null=True)
  timestamp=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.transaction_type} {self.amount} to/from {self.party.name}"