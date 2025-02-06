from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Model_and_tochka, Category, Tag, Order, OrderItem
from django.forms import ModelForm, TextInput, Textarea, inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import Order
from .models import News
from .models import Review

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

from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'status']
        error_messages = {
            'user': {'required': 'Выберите пользователя.'},
            'status': {'required': 'Выберите статус заказа.'},
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        error_messages = {
            'product': {'required': 'Выберите товар.'},
            'quantity': {'required': 'Укажите количество.'},
        }

OrderItemFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True
)



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

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите описание'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишите ваш отзыв...'}),
            'rating': forms.Select(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], attrs={'class': 'form-control'}),
        }
