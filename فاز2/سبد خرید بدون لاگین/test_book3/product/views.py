from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from product.models import *
from basket.forms import BasketAddProductForm


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Book.objects.filter(available=True)
    labels = Book.objects.filter(label='BestSeller')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'labels': labels})


def product_detail(request, id, slug):
    product = get_object_or_404(Book, id=id,
                                slug=slug,
                                available=True)
    basket_product_form = BasketAddProductForm()
    return render(request,
                  'product/detail.html',
                  {'product': product,
                   'basket_product_form': basket_product_form
                   })


class SearchResultsListView(ListView):
    model = Book
    template_name = 'product/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(name__icontains=query)
            | Q(author__icontains=query)
        )
