from django.utils.translation import ugettext_lazy as _, get_language
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib import messages

from ..core.email import email_message
from ..core.sql import SQL
from ..actions.utils import create_action
#from .tasks import asy_email_message
# -----------------------------------
from django.utils.translation import get_language
from django.views.generic import ListView, DetailView
from parler.views import TranslatableSlugMixin
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
#
# from ..core.sql import exc_sql, SQL
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from ..cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(translations__language_code=get_language()).all()
    products = Product.objects.filter(available=True).filter(translations__language_code=get_language()).all()
    if category_slug:
        category = Category.objects.filter(translations__language_code=get_language()).filter(translations__slug=category_slug)[0]
        products = products.filter(category=category)
    return render(request, 'shop/product/product_list.html',
                  {'category': category, 'categories': categories, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, translations__slug=slug, available=True)
    product = Product.objects.filter(translations__language_code=get_language()).filter(translations__slug=slug)[0]
    request.session['product_id'] = product.id
    request.session['product_name'] = product.name
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})

