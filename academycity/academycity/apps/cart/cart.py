from decimal import Decimal
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class Cart(object):
    def __init__(self, request, app_label='abc', model_name='abc'):
        self.model_name = model_name
        self.app_lable = app_label
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, slug=None, s_name=None, coupon_obj=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price), 'slug': slug, 's_name': s_name}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        if coupon_obj and coupon_obj:
            self.cart[product_id]['coupon'] = coupon_obj.code
            self.cart[product_id]['discount'] = coupon_obj.discount
        else:
            self.cart[product_id]['coupon'] = "NA"
            self.cart[product_id]['discount'] = 0
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
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

        product_type = ContentType.objects.get(app_label=self.app_lable, model=self.model_name)
        product_model = product_type.model_class()
        products = product_model.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = Decimal(item['discount'])
            item['total_price'] = item['price'] * item['quantity']
            item['total_discount'] = (item['discount']*item['total_price'])/Decimal('100')
            item['total_price_after_discount'] = item['total_price'] - item['total_discount']
            yield item

    def __len__(self):
            """
            Count all items in the cart.
            """
            return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(item['total_price'] for item in self.cart.values())

    def get_total_discount(self):
        return sum(item['total_discount'] for item in self.cart.values())

    def total_price_after_discount(self):
        return sum(item['total_price_after_discount'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()



