from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from .import views
from .views import order_finish, create_order, ProfileDeletedView

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('catalog/', views.catalog.as_view(), name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register.as_view(), name='register'),
    path('catalog/create', views.createproduct.as_view(), name='createproduct'),
    path('api/', views.api, name='api'),
    path('apidelete', views.apidelete, name='apidelete'),
    path('apicreate', views.apicreate, name='apicreate'),
    path('apiedit', views.apiedit, name='apiedit'),
    path('apiselectmany', views.apiselectmany, name='apiselectmany'),
    path('apiselectone', views.apiselectone, name='apiselectone'),
    path('catalog/<int:pk>/', views.productt.as_view(), name='productt'),
    path('catalog/category/<int:category_id>/', views.FilteredCatalogView.as_view(), name='category'),
    path('catalog/tag/<int:pk>/', views.TagDetailView.as_view(), name='tag'),
    path('catalog/<int:pk>/update', views.update.as_view(), name='update'),
    path('catalog/<int:pk>/delete', views.delete.as_view(), name='delete'),
    path('catalog/createcategory', views.createcategory.as_view(), name='createcategory'),
    path('catalog/CreateTag', views.CreateTag.as_view(), name='CreateTag'),
    path('filter_by_price/', views.filter_by_price, name='filter_by_price'),
    path('order/', views.order.as_view(), name='order'),
    path('create-order/', create_order, name='create_order'),
    path('order-finish/', order_finish, name='order_finish'),
    path('order/create', views.createorder.as_view(), name='createorder'),
    path('order/detail/<int:pk>/', views.detailorder.as_view(), name='detailorder'),
    path('order/update/<int:pk>/', views.updateorder.as_view(), name='updateorder'),
    path('order/delete/<int:pk>/', views.deleteorder.as_view(), name='deleteorder'),

    path('cart/', views.basket_info, name='cart'),
    path('cart/add/<int:product_id>/', views.basket_add, name='add_basket_prod'),
    path('cart/remove/<int:product_id>/', views.basket_remove, name='remove_basket_prod'),
    path('cart/clear/', views.basket_clear, name='clear_basket_prod'),
    path('cart/finish/', order_finish, name='order_finish'),

    path('about_us/', views.about_us, name='about_us'),

    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete-profile/', views.ProfileDeleteView.as_view(), name='delete_profile'),
    path('profile-deleted/', ProfileDeletedView.as_view(), name='profile_deleted'),

    # Api
    path('api/', views.api, name='api'),
    # категории
    path('api/category/', views.ApiCategoryList.as_view(), name='api_category'),
    path('api/category/create/', views.ApiCategoryCreate.as_view(), name='api_category_create'),
    path('api/category/<int:pk>/', views.ApiCategoryDetail.as_view(), name='api_category_detail'),
    path('api/category/update/<int:pk>/', views.ApiCategoryUpdate.as_view(), name='api_category_update'),
    path('api/category/delete/<int:pk>/', views.ApiCategoryDelete.as_view(), name='api_category_delete'),
    # продукты
    path('api/product/', views.ApiModel_and_tochkaList.as_view(), name='api_product'),
    path('api/product/create/', views.ApiModel_and_tochkaCreate.as_view(), name='api_product_create'),
    path('api/product/<int:pk>/', views.ApiModel_and_tochkaDetail.as_view(), name='api_product_detail'),
    path('api/product/update/<int:pk>/', views.ApiCategoryUpdate.as_view(), name='api_product_update'),
    path('api/product/delete/<int:pk>/', views.ApiModel_and_tochkaDelete.as_view(), name='api_product_delete'),
    # тэги
    path('api/tag/', views.ApiTagList.as_view(), name='api_tag'),
    path('api/tag/create/', views.ApiTagCreate.as_view(), name='api_tag_create'),
    path('api/tag/<int:pk>/', views.ApiTagDetail.as_view(), name='api_tag_detail'),
    path('api/tag/update/<int:pk>/', views.ApiTagUpdate.as_view(), name='api_tag_update'),
    path('api/tag/delete/<int:pk>/', views.ApiModel_and_tochkaDelete.as_view(), name='api_tag_delete'),
]