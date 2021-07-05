from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from ..courses.models import CourseSchedule as Product


# this is a cart object.
# you can buils one for every topy with a list of product in the product_model
# see usage in courses app
class BaseCart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_COURSES_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_COURSES_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, user_slug=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price), 'slug': user_slug}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product_id=None):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
            """
            Iterate over the items in the cart and get the products
            from the database.
            """
            product_ids = self.cart.keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)

            cart = self.cart.copy()
            for product in products:
                cart[str(product.id)]['product'] = product

            for item in cart.values():
                item['total_price'] = str(Decimal(item['price']) * item['quantity'])
                yield item

    def __len__(self):
            """
            Count all items in the cart.
            """
            return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_COURSES_ID]
        self.save()

