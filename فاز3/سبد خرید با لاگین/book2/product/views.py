from django.db.models import Q
from orders.models import Invoice, InvoiceItem
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import OrderCreateForm


"""
توضیحات paginate_by مطالعه شود
در تمپلت بیس css عمل نکرد. مسیردهی ها چک شود

"""
class HomeView(ListView):
    model = Book
    # paginate_by = 10
    template_name = "book_list.html"


class BookDetails(DetailView):
    model = Book
    template_name = 'detail.html'


class SearchResultsListView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


"""
میشه مثل مینی پروژه با classview نوشت
اگه اجرا شد برای لیبل جدا بنویس
برای مینی پروژه از dataTables استفاده کردم. همون رو اینجا هم استفاده کن خودش صفحه بندی داره
"""
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Book.objects.filter(available=True)
    labels = Book.objects.filter(label='BestSeller')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'labels': labels})


# it work but not save invoice item
def order_create(request):
    # cart = Cart(request)
    cart = Invoice.objects.get(user=request.user, ordered=False)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                InvoiceItem.objects.create(
                    item=item,
                    user=request.user,
                    ordered=False
                )
            # clear the cart
            cart.clear()
            return render(request,
                          'created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'create.html',
                  {'cart': cart, 'form': form})


# Create your views here.
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Invoice.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "سفارشی ندارید")
            return redirect("/")


# class OrderSummaryView(View):
#     def get(self, *args, **kwargs):
#         order = Invoice.objects.get(ordered=False)
#         return render(self.request, 'order_summary.html', {'object': order})

"""
اینجا میتونی از لینک ajax استفاده کنی(توضیحش خوب بود)
بعد از ثبت با izzitoast پیام بده. برای مینی پروژه ازش استفاده کرده بودم
"""
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_item, created = InvoiceItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Invoice.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "آپدیت شد")
            return redirect("product:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "به سبد خرید اضافه شد")
            return redirect("product:order-summary")
    else:
        ordered_date = timezone.now()
        order = Invoice.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "به سبد خرید اضافه شد")
        return redirect("product:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_qs = Invoice.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = InvoiceItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "آپدیت شد.")
            return redirect("product:order-summary")
        else:
            messages.info(request, "در سبد خرید نیست")
            return redirect("product:product_list", slug=slug)
    else:
        messages.info(request, "سفارشی ندارید")
        return redirect("product:product_list", slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Book, slug=slug)
    order_qs = Invoice.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = InvoiceItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= order_item.quantity
                # order_item.save()
                order_item.delete()
            else:
                order.items.remove(order_item)
            messages.info(request, "آپدیت شد.")
            return redirect("product:order-summary")
        else:
            messages.info(request, "در سبد خرید نیست")
            return redirect("product:product_list", slug=slug)
    else:
        messages.info(request, "سفارشی ندارید")
        return redirect("product:product_list", slug=slug)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid



"""
برای فاز 3 تکمیلش کن

"""
@login_required
def my_orders_view(request):
    qs = Invoice.objects.filter(status='Delivered')
    context = {
        'object': qs
    }
    return render(request, 'my_orders.html', context)
