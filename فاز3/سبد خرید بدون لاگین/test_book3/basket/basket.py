from decimal import Decimal
from django.conf import settings
from product.models import Book
from off.models import DiscountCode, Discount


class Basket(object):

    def __init__(self, request):
        """
        Initialize the basket.
        """
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            # save an empty cart in the session
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket
        # store current applied off_code
        self.off_code_id = self.session.get('off_code_id')

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.basket.keys()
        # get the product objects and add them to the cart
        products = Book.objects.filter(id__in=product_ids)

        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # item['total_price'] = item['discount_book'] * item['quantity']
            # item['dis'] = item['discount_book'] # product.discount_book
            # item['total_price'] = Decimal(item['dis']) * item['quantity']

            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'quantity': 0,
                                       'price': str(product.price)}
        if override_quantity:
            self.basket[product_id]['quantity'] = quantity
        else:
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    @property
    def off_code(self):
        if self.off_code_id:
            try:
                return DiscountCode.objects.get(id=self.off_code_id)
            except DiscountCode.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.off_code:
            return (self.off_code.discount / Decimal(100)) \
                   * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
