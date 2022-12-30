<<<<<<< Updated upstream
from django.db import models
from django.db.models.deletion import SET_NULL
from ckeditor.fields import RichTextField
from django.db.models.fields import CharField
from django.http import request
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F
from archive import settings

class UserStore(AbstractUser):
    store_id = models.IntegerField(null=True, blank=True)
    is_user_store = models.BooleanField(default=False)
    is_admin_store = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    meli = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    agree = models.BooleanField(null=True, blank=True)

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    category = models.ForeignKey(Category,related_name='sub',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubsCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    subcategory = models.ForeignKey(SubCategory,related_name='subs',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubsCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    subscategory = models.ForeignKey(SubsCategory,on_delete=models.SET_NULL,null=True,blank=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    imageone = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagetwo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagethree = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagefour = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    confirmed = models.IntegerField(default=0,null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    countInStock = models.IntegerField(null=True, blank=True)
=======
from django.db import models
from django.db.models.deletion import SET_NULL
from ckeditor.fields import RichTextField
from django.db.models.fields import CharField
from django.http import request
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F
from archive import settings

class UserStore(AbstractUser):
    store_id = models.IntegerField(null=True, blank=True)
    is_user_store = models.BooleanField(default=False)
    is_admin_store = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    meli = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    agree = models.BooleanField(null=True, blank=True)

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    category = models.ForeignKey(Category,related_name='sub',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class SubsCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    subcategory = models.ForeignKey(SubCategory,related_name='subs',on_delete=models.CASCADE)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(SubsCategory, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    subscategory = models.ForeignKey(SubsCategory,on_delete=models.SET_NULL,null=True,blank=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    imageone = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagetwo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagethree = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    imagefour = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    confirmed = models.IntegerField(default=0,null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    countInStock = models.IntegerField(null=True, blank=True)
>>>>>>> Stashed changes
    descreption = RichTextField()