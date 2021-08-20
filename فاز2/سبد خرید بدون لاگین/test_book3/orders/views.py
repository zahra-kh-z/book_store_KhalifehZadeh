from django.shortcuts import render
from django.shortcuts import render
from .models import InvoiceItem
from .forms import OrderCreateForm
from basket.basket import Basket


# Create your views here.

def order_create(request):
    basket = Basket(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in basket:
                InvoiceItem.objects.create(order=order,
                                           product=item['product'],
                                           price=item['price'],
                                           quantity=item['quantity'])
            # clear the basket
            basket.clear()
            return render(request,
                          'order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'order/create.html',
                  {'basket': basket, 'form': form})
