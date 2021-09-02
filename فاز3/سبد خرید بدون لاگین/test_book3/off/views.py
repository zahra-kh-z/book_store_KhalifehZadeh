from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from .models import DiscountCode, Discount
from .forms import DiscountCodeApplyForm


# Create your views here.
@require_POST
def off_code_apply(request):
    """
    With this method, if a discount code has time, it is applied to the shopping cart.
    off_code use in app basket.
    """
    now = timezone.now()
    form = DiscountCodeApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            off_code = DiscountCode.objects.get(code__iexact=code,
                                                valid_from__lte=now,
                                                valid_to__gte=now,
                                                active=True)
            request.session['off_code_id'] = off_code.id
        except DiscountCode.DoesNotExist:
            request.session['off_code_id'] = None
    return redirect('basket:basket_detail')


class DiscountDetailView(DetailView):
    """Shows the details of a discount code."""
    model = Discount
    template_name = 'panel/discount_detail.html'
    login_url = 'login'
