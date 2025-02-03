from django.conf import settings
from .models import Model_and_tochka


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True
        print("Сохранение корзины:", self.basket)  # Отладка: текущее состояние корзины при сохранении

    def add(self, product, count_product=1, update_count=False):
        prod_pk = str(product.pk)

        if prod_pk not in self.basket:
            self.basket[prod_pk] = {
                'count_prod': 0,
                'price_prod': str(product.price)
            }

        if update_count:
            print(f"Обновляем количество товара {product.name} до {count_product}")  # Отладка: обновление количества
            self.basket[prod_pk]['count_prod'] = count_product
        else:
            print(f"Добавляем {count_product} товара {product.name}, текущее количество: {self.basket[prod_pk]['count_prod']}")  # Отладка: добавление количества
            self.basket[prod_pk]['count_prod'] += count_product

        # Проверяем текущее состояние корзины после добавления
        print("Содержимое корзины после добавления:", self.basket)
        self.save()

    def remove(self, product):
        prod_pk = str(product.pk)

        if prod_pk in self.basket:
            print(f"Удаление товара {product.name} из корзины")  # Отладка: удаление товара
            del self.basket[prod_pk]
            self.save()

    def get_total_price(self):
        total_price = sum(float(item['price_prod']) * int(item['count_prod']) for item in self.basket.values())
        print("Итоговая сумма корзины:", total_price)  # Отладка: общая сумма корзины
        return total_price

    def clear(self):
        print("Очистка корзины")  # Отладка: очистка корзины
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        total_count = sum(int(item['count_prod']) for item in self.basket.values())
        print("Общее количество товаров в корзине:", total_count)  # Отладка: общее количество товаров в корзине
        return total_count

    def __iter__(self):
        list_prod_pk = self.basket.keys()
        list_prod_obj = Model_and_tochka.objects.filter(pk__in=list_prod_pk)

        basket = self.basket.copy()

        for prod_obj in list_prod_obj:
            basket[str(prod_obj.pk)]['product'] = prod_obj

        for item in basket.values():
            item['total_price'] = float(item['price_prod']) * int(item['count_prod'])
            print("Товар в корзине:", item)  # Отладка: данные по каждому товару в корзине
            yield item
