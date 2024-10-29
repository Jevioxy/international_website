from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=45, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return '/catalog'


class Model_and_tochka(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория', null=True)
    name = models.CharField(max_length=45, default='Product', verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.FloatField(default=10, verbose_name='Цена')
    data_add = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    data_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    exist = models.BooleanField(default=True, verbose_name='Существует?')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Изображения', blank=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна производителя')

    def __str__(self):
        return f'{self.name} - {self.price}'

    def get_absolute_url(self):
        return f'/catalog/{self.pk}'

    def delete(self, using=None, keep_parents=False):
        self.exist = False
        self.save()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'
        ordering = ['-price', 'name']


class Tag(models.Model):
    name = models.CharField(max_length=45, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    products = models.ManyToManyField('Model_and_tochka', related_name='tags', verbose_name='Товары')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/tag/{self.pk}'

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']



class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    email = models.EmailField(verbose_name='Email пользователя', blank=True, null=True)
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    products = models.ManyToManyField('Model_and_tochka', through='OrderItem', verbose_name='Товары')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='processing', verbose_name='Статус заказа')
    exist = models.BooleanField(default=True, verbose_name='Существует?')

    def __str__(self):
        return f'Order by {self.user.username if self.user else "Unknown"} on {self.creation_date}'

    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email  # Автоматически заполняем поле email почтой пользователя
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Model_and_tochka', on_delete=models.CASCADE, verbose_name='Товар и его цена')
    quantity = models.PositiveIntegerField(verbose_name='Количество товаров на позиции', default=1)


    def __str__(self):
        return f'{self.order} - {self.product}'

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'Позиции заказа'
