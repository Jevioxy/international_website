from django.contrib import admin
from .models import *

# Register your models here.

class Model_and_tochkaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'photo', 'price', 'stock_quantity', 'data_update', 'exist', 'country_of_origin']
    list_display_links = ['name']
    list_editable = ('price', 'exist', 'stock_quantity')
    search_fields = ('name', 'country_of_origin')
    list_filter = ('exist', 'country_of_origin')



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', ]
    list_display_links = ['name']
    search_fields = ('pk', 'name',)


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem
    fk_name = 'order'
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk',  'user', 'email', 'creation_date','status', 'exist',]
    list_display_links = ['user', 'email']
    list_editable = ['status', 'exist']
    search_fields = ('user__username', 'email')
    inlines = [OrderItemAdmin]
    readonly_fields = ['email']  # Делаем поле email только для чтения

    def save_model(self, request, obj, form, change):
        if obj.user:
            obj.email = obj.user.email  # Обновляем email при сохранении модели
        super().save_model(request, obj, form, change)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'text', 'rating', 'creation_date']
    list_display_links = ['user', 'text']
    list_editable = ['rating']
    search_fields = ('user__username', 'text')
    list_filter = ('rating', 'creation_date')

class CountryOfOriginAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    search_fields = ('name',)

class NewsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'publication_date']
    list_display_links = ['title']
    search_fields = ('title', 'description')
    list_filter = ('publication_date',)

@admin.register(ActionHistory)
class ActionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'model_name', 'timestamp', 'details')
    list_filter = ('action_type', 'model_name', 'timestamp')
    search_fields = ('user__username', 'details')




admin.site.register(Review, ReviewAdmin)
admin.site.register(Model_and_tochka, Model_and_tochkaAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(CountryOfOrigin, CountryOfOriginAdmin)
admin.site.register(News, NewsAdmin)