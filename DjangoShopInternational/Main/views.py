from django.contrib.auth import logout
import subprocess
import os
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


class index(ListView):
    model = Model_and_tochka
    template_name = 'Main/index.html'
    context_object_name = 'objects'

    def get_queryset(self):
        # Фильтрация только существующих товаров
        queryset = super().get_queryset()
        queryset = queryset.filter(exist=True)
        return queryset

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




def contact(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_message(form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['subject'], form.cleaned_data['email'], form.cleaned_data['message'])
            context = {'success': True}
        else:
            context['form'] = form
    else:
        form = ContactForm()
        context['form'] = form
    return render(request, 'Contact/contact.html', context=context)



def send_message(name, surname, subject, email, message):
    # Формируем тему и тело письма
    subject = f"WITCH HAPPINES - Новое сообщение: {subject}"
    message_body = f"Имя: {name}\nФамилия: {surname}\nE-mail: {email}\n\nСообщение:\n{message}"

    # Отправляем письмо
    send_mail(
        subject,  # Тема письма
        message_body,  # Текст письма
        settings.DEFAULT_FROM_EMAIL,
        ['t50_n.a.berlikov@mpt.ru'],  # Кому (замените на ваш email)
        fail_silently=False,  # Если ошибка, то она будет выброшена
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

def about_us(request):
    return render(request, 'Main/about_us.html')

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
    template_name = 'AdminPanel/order_form.html'
    success_url = reverse_lazy('adminpanel_order_list')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['order_items'] = OrderItemFormSet(self.request.POST)
        else:
            data['order_items'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['order_items']
        if form.is_valid() and order_items.is_valid():
            with transaction.atomic():
                self.object = form.save()
                order_items.instance = self.object
                order_items.save()
            return super().form_valid(form)
        else:
            # Если есть ошибки, снова отобразим форму с сообщениями об ошибках
            return self.render_to_response(self.get_context_data(form=form))


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

@csrf_exempt
def backup_db(request):
    backup_file_path = os.path.join(settings.BASE_DIR, 'media', 'backups', 'db_backup.json')

    # Если метод запроса GET, вернуть файл резервной копии для скачивания
    if request.method == 'GET':
        if os.path.exists(backup_file_path):
            with open(backup_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/json')
                response['Content-Disposition'] = f'attachment; filename="db_backup.json"'
                return response
        else:
            return JsonResponse({'success': False, 'message': 'Резервная копия не найдена.'})

    # Если метод запроса POST, создать резервную копию базы данных
    elif request.method == 'POST':
        os.makedirs(os.path.dirname(backup_file_path), exist_ok=True)
        try:
            # Создаем резервную копию базы данных
            subprocess.run(
                ['python', 'manage.py', 'dumpdata', '--indent', '2', '-o', backup_file_path],
                check=True
            )
            return JsonResponse({'success': True, 'message': 'Резервная копия успешно создана.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Ошибка при создании резервной копии: {str(e)}'})

def restore_db(request):
    if request.method == 'POST':
        backup_file = request.FILES.get('backup_file')
        if not backup_file:
            return JsonResponse({'success': False, 'message': 'Файл для восстановления не выбран.'})

        temp_path = os.path.join(settings.BASE_DIR, 'temp_backup.json')
        try:
            with open(temp_path, 'wb') as f:
                for chunk in backup_file.chunks():
                    f.write(chunk)
            # Восстановление базы данных
            subprocess.run(['python', 'manage.py', 'loaddata', temp_path], check=True)
            os.remove(temp_path)
            return JsonResponse({'success': True, 'message': 'Восстановление из резервной копии прошло успешно.'})
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return JsonResponse({'success': False, 'message': f'Ошибка при восстановлении из резервной копии: {e}'})

