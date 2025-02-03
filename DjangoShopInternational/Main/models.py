from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class CountryOfOrigin(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название страны')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна происхождения'
        verbose_name_plural = 'Страны происхождения'

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
    country_of_origin = models.ForeignKey(CountryOfOrigin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Страна производителя')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')

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




class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг', default=5)
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отзыв от {self.user.username}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-creation_date']


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    publication_date = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    photo = models.ImageField(upload_to='news_photos/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-publication_date']

class ActionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    action_type = models.CharField(max_length=10, choices=[('create', 'Создание'), ('update', 'Обновление'), ('delete', 'Удаление')], verbose_name='Тип действия')
    model_name = models.CharField(max_length=100, verbose_name='Модель')
    details = models.TextField(verbose_name='Детали')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время действия')

    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.model_name}"