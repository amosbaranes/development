from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from ..cart.cart import Cart
from django.urls import reverse

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
# import weasyprint
from .models import Order


def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    # weasyprint.HTML(string=html).write_pdf(response,
    #                                        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/shop_pdf.css')])
    return response


def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def order_create(request):
    cart = Cart(request, 'shop', 'product')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
            # return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})