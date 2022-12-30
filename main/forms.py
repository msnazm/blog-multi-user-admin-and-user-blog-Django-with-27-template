from django.db import models
from django import forms
from django.db.models import fields
from .models import Store, Category, SubCategory, SubsCategory, Product, OrderItem, ShippingAddress, Review, Templates, ContactUs, ImageBlog
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages 
from ckeditor.widgets import CKEditorWidget

class StoreForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    descreption = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'class': 'form-control'}))

    class Meta:
        model = Store
        fields = ['id','name','slug','image','descreption','datecreate','datecreatealt','user']

class StoreEditForm(forms.ModelForm):
    descreption = forms.CharField(widget=forms.Textarea(attrs={'rows':4,'class': 'form-control'}))

    class Meta:
        model = Store
        fields = ['id','image','descreption']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = '__all__'

class SubCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubCategory
        fields = '__all__'

class SubsCategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubsCategory
        fields = '__all__'

class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    descreption = forms.CharField(widget=CKEditorWidget())
    imageone = forms.ImageField(required=True)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['imageone'] = forms.ImageField(required=True, content_types=['image/png', 'image/jpeg'],max_upload_size=1)
        raise ValidationError('msn')
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass 
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.subcategory.subcategory_set.order_by('name')
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['subscategory'].queryset = SubsCategory.objects.none()
        if 'subcategory' in self.data:
            try:
                subcategory_id = int(self.data.get('subcategory'))
                self.fields['subscategory'].queryset = SubsCategory.objects.filter(subcategory_id=subcategory_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subscategory'].queryset = self.instance.subscategory.subscategory_set.order_by('name')
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(store_id = self.request.user.store_id)
        self.fields['subcategory'].queryset = SubCategory.objects.filter(store_id = self.request.user.store_id)
        self.fields['subscategory'].queryset = SubsCategory.objects.filter(store_id = self.request.user.store_id)
        self.fields['category'].empty_label = 'دسته اصلی را انتخاب کنید'
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = '__all__'

class ShippingAddressForm(forms.ModelForm):
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    postalCode = forms.CharField(required=True)
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['postalCode'] = forms.CharField(required=True, min_length=10, max_length=10)
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'

class TemplateForm(forms.ModelForm):

    class Meta:
        model = Templates
        fields = '__all__'

class ContactUsForm(forms.ModelForm):
    descreption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ContactUs
        fields = '__all__'

class ImageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    imageone = forms.ImageField(required=True)
    
    class Meta:
        model = ImageBlog
        fields = '__all__'
