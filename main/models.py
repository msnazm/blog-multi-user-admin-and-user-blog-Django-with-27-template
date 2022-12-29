from django.db import models
from django.db.models.deletion import SET_NULL
from ckeditor.fields import RichTextField
from django.db.models.fields import CharField
from django.http import request
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum,OuterRef, Subquery, Max, Avg, F
from blog import settings

class UserStore(AbstractUser):
    store_id = models.IntegerField(null=True, blank=True)
    is_user_store = models.BooleanField(default=False)
    is_admin_store = models.BooleanField(default=False)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    meli = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=350, null=True, blank=True)
    agree = models.BooleanField(null=True, blank=True)
    
class Templates(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='image/',blank=True)

class Store(models.Model):
    name = models.CharField(max_length=255)
    templates = models.ForeignKey(Templates,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField(max_length=255,allow_unicode=True,default=0)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    descreption = models.TextField()
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)
    confirmed = models.IntegerField(default=0,null=True, blank=True)

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Store, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


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


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    subscategory = models.ForeignKey(SubsCategory,on_delete=models.SET_NULL,null=True,blank=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    imageone = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,allow_unicode=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    confirmed = models.IntegerField(default=0,null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    descreption = RichTextField()

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

    @property
    def total(self):
        return self.countInStock * self.price

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product-details-store", kwargs={"pk": self.pk,"store_id": self.store_id,"slug": self.slug})   

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True,default=0)
    comment = models.TextField(null=True, blank=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    confirmed = models.IntegerField(default=0,null=True, blank=True)

    def __str__(self):
        return str(self.rating)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    device = models.CharField(max_length=200, null=True, blank=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.BigIntegerField(default=0, null=True, blank=True)
    shippingPrice = models.BigIntegerField(default=0, null=True, blank=True)
    totalPrice = models.BigIntegerField(default=0, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    isfinal = models.BooleanField(default=False)
    finalAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    isfinal = models.BooleanField(default=False)
    price = models.BigIntegerField(null=True, blank=True)
    totalPrice = models.BigIntegerField(null=True, blank=True)
    countInOrder = models.IntegerField(null=True, blank=True)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.product:
            product = self.product
        else:
            product = self.device
        return str(product)

    @property
    def total(self):
        return self.countInOrder * self.price

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=10, null=True, blank=True)
    shippingPrice = models.IntegerField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    selectaddress = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.address)

class ContactUs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    descreption = RichTextField()

    def __str__(self):
        return str(self.descreption)

class ImageBlog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    store = models.ForeignKey(Store,on_delete=models.SET_NULL,null=True)
    imageone = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    name = models.CharField(max_length=255)
    datecreate = models.CharField(max_length=50)
    datecreatealt = models.BigIntegerField()
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name