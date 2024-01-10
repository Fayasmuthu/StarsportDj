
from django import forms
from products.models import ProductImage, Tag
from products.models import Category
from products.models import Product
from main.models import State
from main.models import District
from products.models import Product, AvailableSize


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "image","slug","status",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product Name","class": "form-control"}),
            "slug": forms.TextInput(attrs={"placeholder": "Product Slug","class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product Name","class": "form-control"}),
            "slug": forms.TextInput(attrs={"placeholder": "Product Slug","class": "form-control"}),
            "details": forms.Textarea(attrs={'cols':"30", 'rows':"10"}),
            "meta_title": forms.TextInput(attrs={"placeholder": "Title","class": "form-control"}),
            "meta_description": forms.Textarea(attrs={"placeholder": "Description","class": "form-control",'rows':3}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tag": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.TextInput(attrs={"placeholder": "Product Rating ","class": "form-control",'type':'number','max':5,'min':1}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("title", "background_color",)
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Tag Name","class": "form-control"}),
            "background_color": forms.Select(attrs={"class": "form-select"})
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ("name", "slug",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "State Name","class": "form-control"}),
            "slug": forms.TextInput(attrs={"placeholder": "State Slug","class": "form-control"}),
        }


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ("name", "slug", "state", "delivery_charge",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter District Name","class": "form-control"}),
            "slug": forms.TextInput(attrs={"placeholder": "District Slug","class": "form-control"}),
            "state": forms.Select(attrs={"class": "form-select"}),
            "delivery_charge": forms.TextInput(attrs={"placeholder": "Delivery Charge ","class": "form-control",'type':'number'}),
        }

class AvailableSizeForm(forms.ModelForm):
    class Meta:
        model = AvailableSize
        fields = ('weight', 'unit', 'sale_price', 'regular_price', 'is_stock',)
        widgets = {
            "weight": forms.TextInput(attrs={'required': True,"placeholder": "Weight","class": "required form-control",'type':'number'}),
            "unit": forms.Select(attrs={"class": "required form-select",'required': True}),
            "sale_price": forms.TextInput(attrs={"placeholder": "Sale Price ","class": "required form-control",'type':'number','required': True}),
            "regular_price": forms.TextInput(attrs={"placeholder": "Regular Price ","class": "required form-control",'type':'number','required': True}),
            "is_stock": forms.CheckboxInput(attrs={"class": "form-check-input required",'role':'switch','type':'checkbox'}),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', )
        widgets = {
            "image": forms.FileInput(attrs={"class": "file-input required",'type':'file','required': True}),
            
        }
