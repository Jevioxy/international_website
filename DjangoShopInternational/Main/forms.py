from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Model_and_tochka, Category, Tag, Order, OrderItem
from django.forms import ModelForm, TextInput, Textarea, inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import Order


class Model_and_tochkaForm(ModelForm):


    class Meta:
        model = Model_and_tochka
        fields = ['category', 'name', 'description', 'price', 'photo', 'country_of_origin']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control py-6',
                'placeholder': ''
            }),
            "description": Textarea(attrs={
                'class': 'form-control'
            })
        }

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['description', 'name']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control py-6',
                'placeholder': ''
            }),
            "description": Textarea(attrs={
                'class': 'form-control'
            })
    }
class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['description', 'name', 'products']
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control py-6',
                'placeholder': ''
            }),
            "description": Textarea(attrs={
                'class': 'form-control'
            })
    }

PROD_MAX_COUNT = [(i, str(i)) for i in range(1, 25)]


class BasketAddProductForm(forms.Form):
    count_prod = forms.TypedChoiceField(choices=PROD_MAX_COUNT, coerce=int, label='Количество')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status']  # Поля для выбора пользователя и статуса заказа

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

# Создание formset для OrderItem
OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control py-6'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control py-6'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control py-6'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control py-6'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control py-6'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control py-6'}))


class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=2,
        widget=forms.TextInput(
            attrs={ 'class': 'form-control'}
        )
    )

    surname = forms.CharField(
        min_length=2,
        widget=forms.TextInput(
            attrs={ 'class': 'form-control'}
        )

    )

    subject  = forms.CharField(
        min_length=2,
        widget=forms.TextInput(
            attrs={ 'class': 'form-control'}
        )

    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={ 'class': 'form-control'}
        )
    )
    message = forms.CharField(
        min_length=20,
        widget=forms.Textarea(
            attrs={ 'cols' : 30, 'rows' : 7, 'class': 'form-control'}
        )
    )

class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name', 'email']