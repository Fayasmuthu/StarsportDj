from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView,UpdateView,DetailView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
#forms
from accounts.forms import CustomerAddressForm
from .forms import CustomUserChangeForm
#models
from accounts.models import CustomerAddress
from order.models import Order
from django.contrib.auth.models import User


class AddAddress(View):
    def post(self, request):
        user = request.user
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address_type = form.cleaned_data.get("address_type")
            is_default = form.cleaned_data.get("is_default")
            if CustomerAddress.objects.filter(customer=user).exists():
                if is_default == True:
                    CustomerAddress.objects.filter(customer=user).update(is_default=False)
                if CustomerAddress.objects.filter(customer=user, address_type=address_type).exists():
                    CustomerAddress.objects.filter(customer=user, address_type=address_type).update(
                            **form.cleaned_data
                        )
                else:
                    CustomerAddress.objects.filter(customer=user).create(
                            **form.cleaned_data,customer=user
                        )
                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Address Updated successfully.",
                }
                return JsonResponse(response_data)
            else:
                form.save(commit=False).customer = user
                form.save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Address added successfully.",
                }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)


class AddressListView(LoginRequiredMixin,ListView):
    model = CustomerAddress
    template_name = "account/address.html"
    context_object_name = 'address'

    def get_queryset(self):
        # Filter orders based on the currently logged-in user
        return CustomerAddress.objects.filter(customer=self.request.user)[:2]
    extra_context = {'my_address':True,'form' : CustomerAddressForm()}


def get_address_data(request):
    address_id = request.GET.get('address_id')
    print('address_id=',address_id)
    address = get_object_or_404(CustomerAddress, id=address_id)
    print('address=',address)
    data = {
        'full_name': address.full_name,
        'mobile_no': address.mobile_no,
        'district': address.district.id,
        'city': address.city,
        'address_line_1': address.address_line_1,
        'address_line_2': address.address_line_2,
        'state': address.state.id,
        'pin_code': address.pin_code,
        'is_default': address.is_default,
    }
    return JsonResponse(data)

    
def customer_address_edit(request, pk):
    address = get_object_or_404(CustomerAddress, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST, instance=address)
        if form.is_valid():
            address_type = form.cleaned_data.get("address_type")
            is_default = form.cleaned_data.get("is_default")
            print('is_default',is_default)
            if CustomerAddress.objects.filter(customer=user, address_type=address_type).exists():
                    CustomerAddress.objects.filter(customer=user, address_type=address_type).update(
                        **form.cleaned_data
                    )
            else:
                form.instance.customer = request.user
                form.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Address Updated successfully.",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)


def delete_address(request, pk):
    address = get_object_or_404(CustomerAddress, pk=pk)
    address.delete()
    response_data = {
        "status": "true",
        "title": "Successfully Submitted",
        "message": "Address deleted successfully.",
    }
    return JsonResponse(response_data)


class SettingView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "account/settings.html"  # Specify the template for rendering the form
    success_url = reverse_lazy('accounts:setting')  # Replace with the URL name where you want to redirect after successful form submission
    extra_context = {'my_setting':True}


    def get_object(self, queryset=None):
        return self.request.user
    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Settings updated successfully.",
        }
        return JsonResponse(response_data)  


class UserOrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = "account/orders.html"
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        # Filter orders based on the currently logged-in user
        return Order.objects.filter(user=self.request.user)
    extra_context = {'my_order':True}


class UserOrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    template_name = 'account/order_single.html'
    context_object_name = 'order'
    slug_field = 'order_id'  # Use 'order_id' as the slug field
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        # Further filter orders based on the currently logged-in user
        return Order.objects.filter(user=self.request.user)
    extra_context = {'my_order':True}