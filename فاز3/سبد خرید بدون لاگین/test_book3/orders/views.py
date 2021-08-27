from django.shortcuts import render
from django.shortcuts import render
from .models import InvoiceItem
from .forms import OrderCreateForm
from basket.basket import Basket
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Count

# Create your views here.

@login_required
def order_create(request):
    addr = Address.objects.filter(user=request.user)
    basket = Basket(request)
    if request.method == 'POST':
        # form = OrderCreateForm(request.POST)
        form = OrderCreateForm(request.user, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # order = form.save()
            for item in basket:
                InvoiceItem.objects.create(order=order,
                                           product=item['product'],
                                           price=item['price'],
                                           quantity=item['quantity'],
                                           user_id=request.user.id,
                                           )
            basket.clear()
            return render(request,
                          'order/created.html',
                          {'order': order})
    else:
        # form = OrderCreateForm()
        form = OrderCreateForm(request.user)
    return render(request,
                  'order/create.html',
                  {'basket': basket, 'form': form, "addr": addr,})


@login_required
def user_orders(request):
    user_id = request.user.id
    # orders = Invoice.objects.filter(user_id=user_id).filter(address__default=True).filter(address__user_id=user_id)
    orders = Invoice.objects.filter(user_id=user_id)
    return orders


def all_orders(request):
    orders = Invoice.objects.all()
    orders_count = Invoice.objects.all().count()
    mony = Invoice.objects.all()
    total = sum(product.get_total_cost() for product in mony)
    ord_by_date = Invoice.objects.extra({'created': "date(created)"}).values('created').annotate(count=Count('id'))
    return render(request,
                  'order/all_orders.html',
                  {'orders': orders, 'orders_count': orders_count,
                   'mony': mony,
                   'total':total,
                   'ord_by_date': ord_by_date,
                   })
