from django.contrib.auth import logout
import subprocess
import os
from django.contrib.auth.decorators import user_passes_test
from .forms import NewsForm
from .models import News
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import os
import tempfile
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .basket import Basket
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Order
from .models import *
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView, TemplateView
from .forms import Model_and_tochkaForm, CategoryForm, TagForm, BasketAddProductForm, RegisterUserForm, \
    LoginUserForm, ContactForm, OrderForm, OrderItemFormSet, ProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from rest_framework import generics
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib import messages
from .models import ActionHistory
from . import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order, OrderItem
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


from django.views.generic import ListView
from .models import Model_and_tochka, Review

class index(ListView):
    model = Model_and_tochka
    template_name = 'Main/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(exist=True, stock_quantity__gt=0)  # Фильтрация по наличию
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(is_published=True)[:6]  # Показываем 6 последних отзывов
        return context


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render



from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .models import Model_and_tochka, Category

class catalog(ListView):
    model = Model_and_tochka
    template_name = 'Catalog/catalog.html'
    paginate_by = 6
    context_object_name = 'objects'

    def get_queryset(self):
        # Фильтруем товары, которые есть на складе и существуют
        queryset = super().get_queryset()
        queryset = queryset.filter(exist=True, stock_quantity__gt=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Пагинация
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page', 1)

        try:
            objects = paginator.page(page_number)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['objects'] = objects

        page_links = {
            'first': "?page=1",
            'previous': f"?page={max(1, objects.previous_page_number())}" if objects.has_previous() else None,
            'next': f"?page={min(objects.paginator.num_pages, objects.next_page_number())}" if objects.has_next() else None,
            'last': f"?page={objects.paginator.num_pages}"
        }
        context['page_links'] = page_links

        return context



class FilteredCatalogView(ListView):
    model = Model_and_tochka
    template_name = 'Catalog/catalog.html'
    paginate_by = 3
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Фильтруем по категории и проверяем, что товар существует
        category = self.kwargs.get('category_id')
        queryset = queryset.filter(category_id=category, exist=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        # Пагинация
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page', 1)

        try:
            objects = paginator.page(page_number)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['objects'] = objects

        page_links = {
            'first': "?page=1",
            'previous': f"?page={max(1, objects.previous_page_number())}" if objects.has_previous() else None,
            'next': f"?page={min(objects.paginator.num_pages, objects.next_page_number())}" if objects.has_next() else None,
            'last': f"?page={objects.paginator.num_pages}"
        }
        context['page_links'] = page_links

        return context




from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, ContactForm

def contact(request):
    context = {}
    form = ContactForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        # Если отправлена форма обратной связи
        if 'contact_submit' in request.POST:
            form = ContactForm(request.POST)
            if form.is_valid():
                send_message(
                    form.cleaned_data['name'],
                    form.cleaned_data['surname'],
                    form.cleaned_data['subject'],
                    form.cleaned_data['email'],
                    form.cleaned_data['message']
                )
                return redirect('contact')  # Очищаем форму после отправки

        # Если отправлена форма отзыва
        elif 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user  # Привязываем отзыв к текущему пользователю
                review.save()
                return redirect('contact')  # Перенаправление, чтобы очистить форму

    context['form'] = form
    context['review_form'] = review_form
    context['reviews'] = Review.objects.filter(is_published=True)  # Показываем только опубликованные отзывы
    return render(request, 'Contact/contact.html', context=context)

def send_message(name, surname, subject, email, message):
    subject = f"WITCH HAPPINES - Новое сообщение: {subject}"
    message_body = f"Имя: {name}\nФамилия: {surname}\nE-mail: {email}\n\nСообщение:\n{message}"

    send_mail(
        subject,
        message_body,
        settings.DEFAULT_FROM_EMAIL,
        ['t50_n.a.berlikov@mpt.ru'],  # Замени на свою почту
        fail_silently=False,
    )


class login(LoginView):
    form_class = LoginUserForm
    template_name = 'Login/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return '/catalog/'

def logout_user(request):
    logout(request)
    return redirect('login')


class register(CreateView):
    form_class = RegisterUserForm;
    template_name = 'Login/register.html'
    success_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))


class createproduct(CreateView):
    form_class = Model_and_tochkaForm
    tag_form_class = TagForm
    template_name = 'Catalog/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_form'] = self.tag_form_class()
        return context



class createcategory(CreateView):
    form_class = CategoryForm
    template_name ='Catalog/CreateCategory.html'

class CreateTag(CreateView):
    form_class = TagForm
    template_name = 'Catalog/CreateTag.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def editproduct(request):
    return render(request, 'Catalog/edit.html')

def api(request):
    return render(request, 'Api/api.html')

def apidelete(request):
    return render(request, 'Api/delete.html')

def apicreate(request):
    return render(request, 'Api/create.html')

def apiedit(request):
    return render(request, 'Api/edit.html')

def apiselectmany(request):
    return render(request, 'Api/selectmany.html')

def apiselectone(request):
    return render(request, 'Api/selectone.html')

class productt(DetailView):

    model = Model_and_tochka
    template_name = 'Catalog/shop-singlee.html'
    context_object_name = 'Model_and_tochka'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_form'] = BasketAddProductForm()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'Catalog/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Model_and_tochka.objects.filter(exist=True)
        context['categories'] = Category.objects.all()
        return context

class TagDetailView(DetailView):
    model = Tag
    template_name = 'Catalog/Tag.html'
    context_object_name = 'tag'
    paginate_by = 1  # Количество объектов на одной странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        products = tag.products.all()

        # Создаем экземпляр пагинатора
        paginator = Paginator(products, self.paginate_by)

        # Получаем номер текущей страницы
        page_number = self.request.GET.get('page')

        try:
            # Получаем объекты для текущей страницы
            page_objects = paginator.page(page_number)
        except PageNotAnInteger:
            # Если номер страницы не является целым числом, получаем первую страницу
            page_objects = paginator.page(1)
        except EmptyPage:
            # Если номер страницы не существует, получаем последнюю страницу
            page_objects = paginator.page(paginator.num_pages)

        context['objects'] = page_objects
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        return context


class update(UpdateView):
    model = Model_and_tochka
    template_name = 'Catalog/edit.html'

    form_class = Model_and_tochkaForm

class delete(DeleteView):
    model = Model_and_tochka
    success_url = '/catalog/'
    template_name = 'Catalog/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.exist = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def filter_by_price(request):
    if request.method == 'GET':
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Use reverse to get the correct URL for the view
        return redirect(reverse('filtered_catalog') + f'?min_price={min_price}&max_price={max_price}')




@require_POST
def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Model_and_tochka, pk=product_id)
    form = BasketAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        basket.add(product=product, count_product=cd['count_prod'], update_count=cd['update'])
        return redirect('cart')

def basket_info(request):
    basket = Basket(request)
    return render(request, 'Main/cart.html', {'basket': basket})

def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Model_and_tochka, pk=product_id)
    basket.remove(product)
    return redirect('cart')

def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('cart')

@login_required
@require_POST
def create_order(request):
    basket = Basket(request)

    if not basket or len(basket) == 0:
        print("Корзина пуста, заказ не может быть создан.")
        return redirect('cart')

    # Создаем новый заказ
    order = Order.objects.create(
        user=request.user,
        status='processing'
    )
    print("Создан новый заказ с ID:", order.id)

    # Проходим по товарам в корзине
    for item in basket:
        product = item['product']
        quantity = item['count_prod']

        # Проверяем наличие товара
        if product.stock_quantity < quantity:
            print(f"Недостаточно товара '{product.name}' на складе. Запрошено: {quantity}, Доступно: {product.stock_quantity}")
            return redirect('cart', {'error': f'Недостаточно товара {product.name} на складе.'})

        # Уменьшаем количество на складе только один раз
        print(f"Перед уменьшением: '{product.name}' на складе {product.stock_quantity}, требуется: {quantity}")
        product.stock_quantity -= quantity
        product.save()
        print(f"После уменьшения: '{product.name}' на складе {product.stock_quantity}")

        # Создаем элемент заказа с количеством
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
        print(f"Добавлен товар '{product.name}' в заказ {order.id} в количестве {quantity}")

    # Очищаем корзину
    basket.clear()
    print("Корзина очищена после создания заказа.")

    return redirect('order_finish')

class order(ListView):
    template_name = 'order/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Возвращаем только те заказы, которые существуют
        return Order.objects.filter(status='processing').select_related('user')

class createorder(CreateView):
    form_class = OrderForm
    template_name = 'order/ordercreate.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['order_items'] = OrderItemFormSet(instance=self.object)
        data['products'] = Model_and_tochka.objects.all()  # Получение всех продуктов
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        with transaction.atomic():
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
        # Redirect to the detail view after saving the order
        return redirect(reverse('detailorder', kwargs={'pk': self.object.pk}))

class detailorder(DetailView):
    model = Order
    template_name = 'order/detailorder.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение и проверка всех позиций заказа
        order_items = self.object.orderitem_set.all()
        print(f"Отображение заказа с ID: {self.object.pk} для пользователя: {self.object.user.username}")
        print(f"Всего позиций в заказе: {order_items.count()}")

        for item in order_items:
            print(f"Товар: {item.product.name}, Количество в заказе: {item.quantity}")

        # Добавляем элементы заказа в контекст
        context['order_items'] = order_items

        return context

class updateorder(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/edit.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['order_items'] = OrderItemFormSet(instance=self.object)
        data['products'] = Model_and_tochka.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']

        with transaction.atomic():
            self.object = form.save()

            if order_items.is_valid():
                # Удаляем элементы заказа, которых нет в форме, чтобы избежать дублирования
                order_items.instance = self.object
                existing_items = set(order_items.instance.orderitem_set.values_list('id', flat=True))
                form_item_ids = set([item.instance.id for item in order_items if item.instance.id is not None])

                # Удаляем элементы, не присутствующие в форме
                to_delete = existing_items - form_item_ids
                OrderItem.objects.filter(id__in=to_delete).delete()

                # Сохраняем оставшиеся элементы заказа
                order_items.save()

        return redirect(reverse_lazy('detailorder', kwargs={'pk': self.object.pk}))

class deleteorder(DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = '/order/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.exist = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

# категория

class ApiCategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ApiCategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ApiCategoryCreate(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ApiCategoryUpdate(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

class ApiCategoryDelete(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

# продукы

class ApiModel_and_tochkaList(generics.ListAPIView):
    queryset = Model_and_tochka.objects.all()
    serializer_class = serializers.Model_and_tochkaSerializer

class ApiModel_and_tochkaDetail(generics.RetrieveAPIView):
    queryset = Model_and_tochka.objects.all()
    serializer_class = serializers.Model_and_tochkaSerializer

class ApiModel_and_tochkaCreate(generics.CreateAPIView):
    queryset = Model_and_tochka.objects.all()
    serializer_class = serializers.Model_and_tochkaSerializer

class ApiModel_and_tochkaUpdate(generics.RetrieveAPIView):
    queryset = Model_and_tochka.objects.all()
    serializer_class = serializers.Model_and_tochkaSerializer

class ApiModel_and_tochkaDelete(generics.RetrieveDestroyAPIView):
    queryset = Model_and_tochka.objects.all()
    serializer_class = serializers.Model_and_tochkaSerializer

# Тэг
class ApiTagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ApiTagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ApiTagCreate(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ApiTagUpdate(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ApiTagDelete(generics.RetrieveDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

# заказы
class ApiOrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
class ApiOrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
class ApiOrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
class ApiOrderUpdate(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
class ApiOrderDelete(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

#  ММ заказы
class ApiOrderItemList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
class ApiOrderItemDetail(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
class ApiOrderItemCreate(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
class ApiOrderItemUpdate(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
class ApiOrderItemDelete(generics.RetrieveDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

def order_finish(request):
    return render(request, 'Main/orderfinish.html')


from .models import Review

def about_us(request):
    reviews = Review.objects.filter(is_published=True)  # Показываем только одобренные отзывы
    return render(request, 'Main/about_us.html', {'reviews': reviews})


def example(request):
    return render(request, 'Main/a.html')

def profile(request):
    return render(request, 'Main/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Замените 'profile' на нужный URL или имя представления
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'Main/edit_profile.html', {'form': form})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'Main/profile_confirm_delete.html'
    success_url = reverse_lazy('profile_deleted')  # перенаправление на страницу после удаления профиля

    def get_object(self, queryset=None):
        # Удаляем только текущего пользователя
        return self.request.user

class ProfileDeletedView(TemplateView):
    template_name = 'Main/profile_deleted.html'



# Проверка на суперпользователя
@user_passes_test(lambda u: u.is_superuser)
@login_required
def admin_panel(request):
    return render(request, 'AdminPanel/adminpanel.html')

# Проверка на доступ только для суперпользователей
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AdminPanelOrderListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Order
    template_name = 'AdminPanel/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10  # Пагинация

    def get_queryset(self):
        return Order.objects.filter(exist=True).select_related('user')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class AdminPanelOrderCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'AdminPanel/order_create.html'
    success_url = reverse_lazy('adminpanel_order_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Передаём в контекст форму для позиций товаров
        """
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST)
        else:
            data['order_items'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        """
        Обрабатываем форму и сохраняем связанные элементы заказа
        """
        context = self.get_context_data()
        order_items = context['order_items']
        if form.is_valid() and order_items.is_valid():
            with transaction.atomic():
                self.object = form.save()
                order_items.instance = self.object
                order_items.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))



from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Order, OrderItem, Model_and_tochka
from .forms import OrderForm, OrderItemForm

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import UpdateView
from django.db import transaction
from django.urls import reverse_lazy
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemFormSet


from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Order
from .forms import OrderForm

class AdminPanelOrderUpdateStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm  # Оставляем только форму заказа без товаров
    template_name = 'AdminPanel/order_edit_status.html'
    success_url = reverse_lazy('adminpanel_order_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        """
        Обновляем только статус заказа.
        """
        self.object = form.save()
        return redirect(self.success_url)

from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderItemForm

OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)

class AdminPanelOrderUpdateItemsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    template_name = 'AdminPanel/order_edit_items.html'
    fields = []  # Здесь не нужно указывать поля, так как мы работаем только с OrderItem

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Передаём в контекст форму для позиций товаров
        """
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['order_items'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Сохраняем изменения в товарах заказа
        """
        context = self.get_context_data()
        order_items = context['order_items']
        if order_items.is_valid():
            with transaction.atomic():
                order_items.instance = self.object
                order_items.save()
            return redirect('adminpanel_order_list')
        return self.render_to_response(self.get_context_data(form=form))



class AdminPanelOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    template_name = 'AdminPanel/order_confirm_delete.html'
    success_url = reverse_lazy('adminpanel_order_list')

    def test_func(self):
        return self.request.user.is_superuser



class NewsListView(ListView):
    model = News
    template_name = 'Contact/news.html'
    context_object_name = 'news_list'
    paginate_by = 6

class NewsDetailView(DetailView):
    model = News
    template_name = 'Contact/news_detail.html'
    context_object_name = 'news'

class WarehouseListView(UserPassesTestMixin, ListView):
    model = Model_and_tochka
    template_name = 'Main/warehouse.html'
    context_object_name = 'products'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Model_and_tochka.objects.filter(exist=True)

    # Обработчик AJAX-запроса для обновления количества
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        new_quantity = request.POST.get('new_quantity')

        try:
            product = Model_and_tochka.objects.get(id=product_id)
            product.stock_quantity = new_quantity
            product.save()
            return JsonResponse({'success': True, 'new_quantity': product.stock_quantity})
        except Model_and_tochka.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})

class EditStockView(UpdateView):
    model = Model_and_tochka
    fields = ['stock_quantity']
    template_name = 'Main/edit_stock.html'
    success_url = reverse_lazy('warehouse')

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class ActionHistoryView(ListView):
    model = ActionHistory
    template_name = 'Main/action_history.html'
    context_object_name = 'actions'
    paginate_by = 10  # Если нужно добавить пагинацию

    def get_queryset(self):
        return ActionHistory.objects.order_by('-timestamp')

@login_required
def action_history(request):
    # Получаем историю действий, сортируем от новых к старым
    records = ActionHistory.objects.all().order_by('-timestamp')
    return render(request, 'Main/action_history.html', {'records': records})

@login_required
def delete_action_history(request, pk):
    action_history = get_object_or_404(ActionHistory, pk=pk)
    action_history.delete()
    return redirect(reverse('action_history'))

@login_required
def clear_action_history(request):
    ActionHistory.objects.all().delete()  # Удаляем все записи из таблицы
    messages.success(request, "История действий успешно очищена.")
    return redirect('action_history')  # Перенаправляем обратно на страницу истории

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Model_and_tochka, pk=pk)
    product.delete()
    messages.success(request, "Товар успешно удалён.")
    return redirect('warehouse')

# Проверка на доступ только для суперпользователей
def admin_required(user):
    return user.is_superuser

@method_decorator(user_passes_test(admin_required), name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'AdminPanel/user_list.html'
    context_object_name = 'users'


@method_decorator(user_passes_test(admin_required), name='dispatch')
class UserCreateView(CreateView):
    model = User
    template_name = 'AdminPanel/user_form.html'
    fields = ['username', 'email', 'is_staff', 'is_active']
    success_url = reverse_lazy('user_list')

@method_decorator(user_passes_test(admin_required), name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'AdminPanel/user_form.html'
    fields = ['username', 'email', 'is_staff', 'is_active']
    success_url = reverse_lazy('user_list')

@user_passes_test(admin_required)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('user_list')


import json
import subprocess
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.core.serializers import serialize
from django.apps import apps

@csrf_exempt
def backup_db(request):
    """
    Создание резервной копии базы данных и скачивание без сохранения на сервере.
    """
    try:
        # Выбираем модели, которые нужно сохранить
        models_to_backup = ["Main.Category", "Main.CountryOfOrigin", "Main.Model_and_tochka",
                            "Main.Order", "Main.OrderItem", "Main.Review", "Main.News", "Main.ActionHistory"]

        # Создаём резервную копию в памяти (без сохранения на сервере)
        backup_data = []
        for model_name in models_to_backup:
            model = apps.get_model(model_name)
            serialized_data = json.loads(serialize("json", model.objects.all()))

            # Преобразуем внешние ключи в объекты
            for obj in serialized_data:
                fields = obj["fields"]

                # Меняем category и country_of_origin
                if "category" in fields and fields["category"]:
                    category = Category.objects.filter(pk=fields["category"]).first()
                    if category:
                        fields["category"] = {"pk": category.pk, "name": category.name, "description": category.description}

                if "country_of_origin" in fields and fields["country_of_origin"]:
                    country = CountryOfOrigin.objects.filter(pk=fields["country_of_origin"]).first()
                    if country:
                        fields["country_of_origin"] = {"pk": country.pk, "name": country.name}

            backup_data.extend(serialized_data)

        # Записываем в файл (для скачивания)
        json_output = json.dumps(backup_data, ensure_ascii=False, indent=2)
        response = HttpResponse(json_output, content_type="application/json")
        response["Content-Disposition"] = 'attachment; filename="db_backup.json"'

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Ошибка при создании резервной копии: {e}'})


import json
import io
import subprocess
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Category, CountryOfOrigin, Model_and_tochka, Order, OrderItem, Review, News, ActionHistory
from django.db import transaction, IntegrityError

@csrf_exempt
def backup_db(request):
    """
    Создание резервной копии и отправка пользователю без сохранения на сервере.
    """
    try:
        output = subprocess.run(
            ['python', 'manage.py', 'dumpdata', '--indent', '2'],
            capture_output=True,
            text=True,
            check=True
        )
        response = HttpResponse(output.stdout, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="db_backup.json"'
        return response
    except subprocess.CalledProcessError as e:
        return JsonResponse({'success': False, 'message': f'Ошибка при создании резервной копии: {e}'})

import json
from django.db import transaction, connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import (
    Model_and_tochka, Order, OrderItem, Review, News,
    ActionHistory, Category, CountryOfOrigin
)


@csrf_exempt
def restore_db(request):
    """
    Восстановление базы данных из загруженной резервной копии.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Неверный метод запроса'})

    backup_file = request.FILES.get('backup_file')
    if not backup_file:
        return JsonResponse({'success': False, 'message': 'Файл для восстановления не выбран.'})

    try:
        # Загружаем JSON из загруженного файла
        data = json.load(backup_file)

        print("⚠️ НАЧИНАЕМ ВОССТАНОВЛЕНИЕ...\n")

        with transaction.atomic():
            # Очистка таблиц, кроме пользователей
            print(f"📊 Перед очисткой: {Model_and_tochka.objects.count()} товаров, {Category.objects.count()} категорий")

            Model_and_tochka.objects.all().delete()
            Order.objects.all().delete()
            OrderItem.objects.all().delete()
            Review.objects.all().delete()
            News.objects.all().delete()
            ActionHistory.objects.all().delete()
            Category.objects.all().delete()
            CountryOfOrigin.objects.all().delete()

            print(f"✅ Очистка завершена. Товаров: {Model_and_tochka.objects.count()}, Категорий: {Category.objects.count()}\n")

            # Восстанавливаем пользователей ПЕРВЫМИ
            users = []
            user_groups = {}  # Храним группы
            user_permissions = {}  # Храним права доступа

            for item in data:
                if item["model"] == "auth.user":
                    user_data = item["fields"]
                    groups = user_data.pop("groups", [])  # Извлекаем группы
                    permissions = user_data.pop("user_permissions", [])  # Извлекаем права

                    user, _ = User.objects.update_or_create(id=item["pk"], defaults=user_data)
                    user_groups[user.id] = groups
                    user_permissions[user.id] = permissions

            # Присваиваем группы и права пользователям
            for user_id, groups in user_groups.items():
                user = User.objects.filter(id=user_id).first()
                if user:
                    user.groups.set(groups)

            for user_id, permissions in user_permissions.items():
                user = User.objects.filter(id=user_id).first()
                if user:
                    user.user_permissions.set(permissions)

            print(f"✅ Восстановлено пользователей: {len(users)}\n")

            # Восстанавливаем категории и страны
            categories = []
            countries = []
            objects_to_create = []

            for item in data:
                model_name = item["model"]
                fields = item["fields"]

                if model_name == "Main.category":
                    category, _ = Category.objects.update_or_create(id=item["pk"], defaults=fields)
                    categories.append(category)
                elif model_name == "Main.countryoforigin":
                    country, _ = CountryOfOrigin.objects.update_or_create(id=item["pk"], defaults=fields)
                    countries.append(country)
                else:
                    objects_to_create.append(item)

            print(f"✅ Восстановлено категорий: {len(categories)}, стран: {len(countries)}\n")

            # Восстанавливаем остальные данные
            for item in objects_to_create:
                model_name = item["model"]
                fields = item["fields"]

                if model_name == "Main.model_and_tochka":
                    fields["category"] = Category.objects.get(id=fields["category"]) if fields["category"] else None
                    fields["country_of_origin"] = CountryOfOrigin.objects.get(id=fields["country_of_origin"]) if fields["country_of_origin"] else None
                    Model_and_tochka.objects.update_or_create(id=item["pk"], defaults=fields)

                elif model_name == "Main.order":
                    fields["user"] = User.objects.filter(id=fields["user"]).first()
                    Order.objects.update_or_create(id=item["pk"], defaults=fields)

                elif model_name == "Main.orderitem":
                    fields["order"] = Order.objects.get(id=fields["order"])
                    fields["product"] = Model_and_tochka.objects.get(id=fields["product"])
                    OrderItem.objects.update_or_create(id=item["pk"], defaults=fields)

                elif model_name == "Main.review":
                    fields["user"] = User.objects.filter(id=fields["user"]).first()
                    Review.objects.update_or_create(id=item["pk"], defaults=fields)

                elif model_name == "Main.news":
                    News.objects.update_or_create(id=item["pk"], defaults=fields)

                elif model_name == "Main.actionhistory":
                    fields["user"] = User.objects.filter(id=fields["user"]).first()
                    ActionHistory.objects.update_or_create(id=item["pk"], defaults=fields)

            print(f"✅ Восстановлено товаров: {Model_and_tochka.objects.count()}, заказов: {Order.objects.count()}\n")

            # Сбрасываем автоинкремент для всех таблиц
            reset_auto_increment()

        return JsonResponse({'success': True, 'message': 'Восстановление из резервной копии прошло успешно.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Ошибка при восстановлении: {e}'})


def reset_auto_increment():
    """
    Автоматический сброс автоинкремента для всех таблиц после восстановления.
    """
    tables = [
        "Main_model_and_tochka",
        "Main_order",
        "Main_review",
        "Main_actionhistory",
        "Main_category",
        "Main_countryoforigin",
        "Main_orderitem",
        "Main_news"
    ]

    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"SELECT setval(pg_get_serial_sequence('\"{table}\"', 'id'), (SELECT MAX(id) FROM \"{table}\")+1);")
            print(f"✅ Автоинкремент сброшен для {table}")



def create_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')  # Перенаправление на страницу списка новостей
    else:
        form = NewsForm()

    return render(request, 'Contact/news_create.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)  # Ограничиваем доступ только для staff
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)  # Перенаправление на просмотр новости
    else:
        form = NewsForm(instance=news)

    return render(request, 'Contact/news_edit.html', {'form': form, 'news': news})

@user_passes_test(lambda u: u.is_staff)  # Доступ только для staff
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    return redirect('news_list')  # Перенаправление на список новостей после удаления

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Review
from .forms import ReviewForm

# Проверка, является ли пользователь администратором
def admin_required(user):
    return user.is_staff

@login_required
@user_passes_test(admin_required)
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'Adminpanel/review_list.html', {'reviews': reviews})

@login_required
@user_passes_test(admin_required)
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('adminpanel_review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'Adminpanel/review_edit.html', {'form': form, 'review': review})

@login_required
@user_passes_test(admin_required)
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('adminpanel_review_list')
    return render(request, 'Adminpanel/review_confirm_delete.html', {'review': review})

@login_required
@user_passes_test(admin_required)
def review_toggle_publish(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.is_published = not review.is_published
    review.save()
    return redirect('adminpanel_review_list')
