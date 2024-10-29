from django.conf import settings
from .models import *


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

    def add(self, product, count_product=1, update_count=False):
        prod_pk = str(product.pk)

        if prod_pk not in self.basket:
            self.basket[prod_pk] = {
                'count_prod': 0,
                'price_prod': str(product.price)
            }

        if update_count:
            self.basket[prod_pk]['count_prod'] = count_product
        else:
            self.basket[prod_pk]['count_prod'] += count_product

        self.save()

    def remove(self, product):
        prod_pk = str(product.pk)

        if prod_pk in self.basket:
            del self.basket[prod_pk]
            self.save()

    def get_total_price(self):
        return sum(float(item['price_prod']) * int(item['count_prod']) for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def __len__(self):
        return sum(int(item['count_prod']) for item in self.basket.values())

    def __iter__(self):
        list_prod_pk = self.basket.keys()

        list_prod_obj = Model_and_tochka.objects.filter(pk__in=list_prod_pk)

        basket = self.basket.copy()

        for prod_obj in list_prod_obj:
            basket[str(prod_obj.pk)]['product'] = prod_obj

        for item in basket.values():
            item['total_price'] = float(item['price_prod']) * int(item['count_prod'])
            yield item
