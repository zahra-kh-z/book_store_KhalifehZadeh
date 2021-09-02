from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import OrderCreateForm
from basket.basket import Basket
from .models import *
from django.db.models import Count


# Create your views here.
@login_required
def order_create(request):
    """
    crete an order by item of basket and show address of user for send orders.
    """
    addr = Address.objects.filter(user=request.user)
    basket = Basket(request)
    # cart = Invoice.objects.get(user=request.user, ordered=False)
    # address = Invoice.objects.get(user=request.user, address__default=True)
    if request.method == 'POST':
        form = OrderCreateForm(request.user, request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in basket:
                order_item = InvoiceItem.objects.create(order=order,
                                                        product=item['product'], price=item['price'],
                                                        quantity=item['quantity'], user_id=request.user.id, )

                # Reduce stock when order is placed or saved
                products = Book.objects.get(id=order_item.product_id)
                if products.inventory > order_item.quantity:
                    products.inventory = int(order_item.product.inventory - order_item.quantity)

                products.save()

            # clear the basket
            basket.clear()
            return render(request, 'order/created.html', {'order': order, })
    else:
        form = OrderCreateForm(request.user)

    return render(request, 'order/create.html', {'basket': basket, 'form': form, "addr": addr, })


@login_required
def user_orders(request):
    """all orders of one user"""
    user_id = request.user.id
    orders = Invoice.objects.filter(user_id=user_id)
    return orders


def all_orders(request):
    """
    for report of orders in admin panel
    total price of sale orders
    and orders by date
    """
    # total price
    orders = Invoice.objects.all()
    orders_count = Invoice.objects.all().count()
    mony = Invoice.objects.all()
    total = sum(product.get_total_cost() for product in mony)

    # orders by date
    ord_by_date = Invoice.objects.extra({'created': "date(created)"}).values('created').annotate(count=Count('id'))

    # from django.db.models import F, Q
    # ord_by_date=(Invoice.objects.annotate(created__day=F('created__day')).annotate(total=Count('id'))
    #  .filter(total__gt=0))
    # ord_by_date = (Invoice.objects.annotate(created__day=Count('id')).values('id', 'created__day'))

    return render(request,
                  'order/all_orders.html',
                  {'orders': orders, 'orders_count': orders_count,
                   'mony': mony, 'total': total,
                   'ord_by_date': ord_by_date,
                   })
