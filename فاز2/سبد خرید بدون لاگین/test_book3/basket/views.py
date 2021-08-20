from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Book
from .basket import Basket
from .forms import BasketAddProductForm
from off.forms import DiscountCodeApplyForm
from product.models import *


@require_POST
def basket_add(request, product_id):
    """
    for add one row to basket list
    """
    basket = Basket(request)
    product = get_object_or_404(Book, id=product_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        cdata = form.cleaned_data
        basket.add(product=product,
                   quantity=cdata['quantity'],
                   override_quantity=cdata['override'])
    return redirect('basket:basket_detail')


@require_POST
def basket_remove(request, product_id):
    """
        for remove row from basket
    """
    basket = Basket(request)
    product = get_object_or_404(Book, id=product_id)
    basket.remove(product)
    return redirect('basket:basket_detail')


# def basket_detail(request):
#     basket = Basket(request)
#     return render(request, 'basket/detail.html', {'basket': basket})

def basket_detail(request):
    basket = Basket(request)
    for item in basket:
        item['update_quantity_form'] = BasketAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    off_apply_form = DiscountCodeApplyForm()
    return render(request, 'basket/detail.html', {'basket': basket,
                                                  'off_apply_form': off_apply_form
                                                  })


def basket_history(request):
    user_basket = Basket.objects.filter(session=request.session.session_key[:30])
    total = 0
    for item in user_basket:
        total += item.quantity * item.price
    return render('basket/history.html', {'user_basket': user_basket, 'total': total})
