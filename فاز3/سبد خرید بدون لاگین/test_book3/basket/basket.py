from decimal import Decimal
from django.conf import settings
from product.models import Book
from off.models import DiscountCode, Discount

"""
When users log in to the site, their anonymous session is lost and a new session is created for authenticated users. 
If you store items in an anonymous session that you need to keep after the user logs in, 
you will have to copy the old session data into the new session. 
You can do this by retrieving the session data before you log in the user using 
the login() function of the Django authentication system and storing it in the session after that.
"""


class Basket(object):

    def __init__(self, request):

        """
        You store the current session using self.session = request.session 
        to make it accessible to the other methods of the basket class.
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
        In this method, you retrieve the Product instances that are present
        in the basket to include them in the basket items.

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
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.basket.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        You convert the product ID into a string because Django uses JSON to serialize session data, and
        JSON only allows string key names.
        The product's price is converted from decimal into a string in order to serialize it.
        override_quantity: This is a Boolean that indicates whether the quantity
        needs to be overridden with the given quantity (True), or whether the new
        quantity has to be added to the existing quantity (False).
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
        """mark the session as "modified" to make sure it gets saved"""
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
        """remove cart from session"""
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        """total price for all item in basket"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

    @property
    def off_code(self):
        """add off code for final basket price"""
        if self.off_code_id:
            try:
                return DiscountCode.objects.get(id=self.off_code_id)
            except DiscountCode.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """add discount for final basket price by off code"""
        if self.off_code:
            return (self.off_code.discount / Decimal(100)) \
                   * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """total price after add off code on basket"""
        return self.get_total_price() - self.get_discount()
