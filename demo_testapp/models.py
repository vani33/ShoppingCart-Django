from django.db import models
import datetime, os
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Search(models.Model):
     search = models.CharField(max_length=500)
     created = models.DateTimeField(auto_now=True)

     def __str__(self):
         return '{}'.format(self.search)

class EasyCartUsersInfo(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    email = models.EmailField(max_length=30)
    mobileNo = models.IntegerField()
    city = models.CharField(max_length=15)

class Category(models.Model):
    nameOfCategory = models.CharField(max_length=20)
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children',on_delete=models.CASCADE)

    def __str__(self):
      return self.nameOfCategory

class Product(models.Model):
    nameOfProduct = models.CharField(max_length=20)
    category = models.ForeignKey('Category',on_delete=models.PROTECT)
    image = models.ImageField(upload_to="demo_testapp/images", null=True, blank=True)
    price = models.FloatField()
    quantity = models.FloatField()

    def __unicode__(self):
        return self.__unicode__()

class UsersProductsInfoManager(models.Manager):
    def create_cart(self,user,category,nameOfProduct,image,price,quantity):
        obj = self.model()
        obj.user = user
        obj.category=category
        obj.nameOfProduct = nameOfProduct
        obj.image=image
        obj.price=price
        obj.quantity=quantity
        obj.save()
        return obj
    def create_wishlist(self,user,category,nameOfProduct,image,price,quantity):
        obj = self.model()
        obj.user = user
        obj.category = category
        obj.nameOfProduct = nameOfProduct
        obj.image = image
        obj.price = price
        obj.quantity = quantity
        obj.save()
        return obj

class UsersProductsCartInfo(models.Model):
    user = models.ForeignKey('EasyCart',related_name='userCart',on_delete=models.PROTECT)
    category = models.CharField(max_length=20)
    nameOfProduct = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.FloatField()

    objects = UsersProductsInfoManager()
    def __unicode__(self):
        return self.__unicode__()

class UsersProductsWishlistInfo(models.Model):
    user = models.ForeignKey('EasyCart',related_name='userWishlist',on_delete=models.PROTECT)
    category = models.CharField(max_length=20)
    nameOfProduct = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.FloatField()

    objects = UsersProductsInfoManager()
    def __unicode__(self):
        return self.__unicode__()

class EasyCartManager(BaseUserManager):
    def create_user(self, email,userName,firstName,lastName, mobileNo, city, password=None, is_active=True, is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not firstName:
            raise ValueError("Users must have a First name")
        if not lastName:
            raise ValueError("Users must have a Lastname")
        if not mobileNo:
            raise ValueError("Users must have a mobile Number")
        if not city:
            raise ValueError("Users must have a city")
        user_obj = self.model(email = self.normalize_email(email))
        user_obj.userName = userName
        user_obj.firstName = firstName
        user_obj.lastName = lastName
        user_obj.mobileNo = mobileNo
        user_obj.city = city
        user_obj.set_password(password) #change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, userName, firstName, lastName, mobileNo, city, password=None):
        user_obj = self.create_user(email,userName,firstName,lastName, mobileNo, city,password=password,is_staff=True)
        return user_obj

    def create_superuser(self, email, userName, firstName, lastName, mobileNo, city, password=None):
        user_obj = self.create_user(email, userName,firstName, lastName, mobileNo, city, password=password, is_staff=True, is_admin=True)
        return user_obj

class EasyCart(AbstractBaseUser):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=20)
    mobileNo = models.IntegerField()
    city = models.CharField(max_length=15)

    email = models.EmailField(max_length=30, unique=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #non super user
    admin = models.BooleanField(default=False) #super user
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username
    REQUIRED_FIELDS = ['userName','firstName','lastName','mobileNo','city'] #USERNAME_FIELD and password are required by default

    objects = EasyCartManager()

    def __str__(self):
        return self.email
    def get_firstName(self):
        return self.firstName
    def get_lastName(self):
        return self.lastName

    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
