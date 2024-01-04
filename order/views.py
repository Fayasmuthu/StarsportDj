
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
import requests
from accounts.forms import CustomerAddressForm

from products.models import AvailableSize
from order.models import CartItem, OrderItem, Payment, Wishlist,Order
from accounts.models import CustomerAddress

#cart
class CartView(LoginRequiredMixin, View):
    template_name = "web/cart.html"

    def get(self, request):
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user)
        cart_total = float(sum(item.get_total_price() for item in CartItem.objects.filter(user=user)))
        context = {
            "cart_items": cart_items,
            "cart_total": cart_total
        }
        return render(request, self.template_name, context)


class AddToCartView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        quantity = request.GET.get('quantity', 1)
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(AvailableSize, pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults=({"quantity": quantity})
        )

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        return JsonResponse({
            'message': 'Product Quantity Added from cart successfully',
            'quantity':cart_item.quantity,
            'total_price':cart_item.get_total_price(),
            'cart_total':cart_item.cart_total(),
            'cart_count':CartItem.objects.filter(user=request.user).count(),
            'wishlist_count':Wishlist.objects.filter(user=request.user).count()
        })


class MinusCartView(LoginRequiredMixin,View):
   def get(self, request):
        try:
            cart_id = request.GET.get("cart_id")
            cart_item = CartItem.objects.get(id=cart_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            return JsonResponse({'message': 'Product Quantity decreased from cart successfully','quantity':cart_item.quantity,'total_price':cart_item.get_total_price(),'cart_total':cart_item.cart_total()})
        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Product not found in cart'}, status=404)
        

class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, cart_item_id, *args, **kwargs):
        user = self.request.user
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=user)
        cart_item.delete()
        return redirect("order:cart")


class ClearCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        user = request.user
        CartItem.objects.filter(user=user).delete()
        return redirect('order:cart') 
    
#wishlist
class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView( View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(AvailableSize, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            return JsonResponse({'message': 'Product Added from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.'})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        return JsonResponse({'message': 'Product Removed from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})



class CheckoutView(LoginRequiredMixin, View):
    template_name = "web/shop-checkout.html"

    def get(self, request):
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user)
        form = CustomerAddressForm()
        address = None
        if CustomerAddress.objects.filter(customer=user).exists():
            address = CustomerAddress.objects.filter(customer=user)[:2]
        cart_total = float(sum(item.get_total_price() for item in CartItem.objects.filter(user=user)))
        context = {
            "cart_items": cart_items,
            "cart_total": cart_total ,
            "form": form,
            "address": address
        }
        return render(request, self.template_name, context)


class OrderCreateView(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        selected_address = self.request.POST.get("selected_address")
        selected_payment = self.request.POST.get("selected_payment")
        item_subtotal = self.request.POST.get("item_subtotal")
        service_fee = self.request.POST.get("service_fee")
        shipping_fee = self.request.POST.get("shipping_fee")
        total_amt = self.request.POST.get("total_amt")
        cart_items = CartItem.objects.filter(user=user)
        data = Order.objects.create(
            user=user,
            address=CustomerAddress.objects.get(id=selected_address),
            item_subtotal=item_subtotal,
            service_fee=service_fee,
            shipping_fee=shipping_fee
        )
        order_items_list = []
        for cart_item in cart_items:
            order_item = {
                "name": str(cart_item.product.product.name) + " / " + str(cart_item.product.weight) + " " + str(cart_item.product.unit),
                "sku": str(cart_item.product.id),
                "units": str(cart_item.quantity),
                "selling_price": str(cart_item.product.sale_price),
                "discount": "0",  # You may adjust this based on your requirements
                "tax": "0",  # You may adjust this based on your requirements
                "hsn": ""  # You may adjust this based on your requirements
            }
            order_items_list.append(order_item)
            OrderItem.objects.create(
                order=data,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.sale_price
            )
            cart_item.delete()
        payment_data = Payment.objects.create(
            order=data,
            payment_method=selected_payment,
            amount=total_amt
        )
        url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"
        payload = json.dumps({
            "order_id": str(data.order_id), 
            "order_date": str(data.timestamp),
            "pickup_location": "Test",
            "channel_id": "4532346",
            "comment": "fast and furious",
            "billing_customer_name": str(data.address.full_name),
            "billing_last_name": "",
            "billing_address": str(data.address.address_line_1),
            "billing_address_2": str(data.address.address_line_2),
            "billing_city": str(data.address.city),
            "billing_pincode": str(data.address.pin_code),
            "billing_state": str(data.address.state.name),
            "billing_country": "india",
            "billing_email": str(data.user.email),
            "billing_phone": str(data.address.mobile_no),
            "shipping_is_billing": 1,
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": order_items_list,
            "payment_method": str(payment_data.payment_method),
            "shipping_charges": str(shipping_fee),
            "giftwrap_charges": "",
            "transaction_charges": "",
            "total_discount": "",
            "sub_total": str(total_amt),
            "length": "10",
            "breadth": "10",
            "height": "10",
            "weight": "1.5"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaXYyLnNoaXByb2NrZXQuaW4vdjEvZXh0ZXJuYWwvYXV0aC9sb2dpbiIsImlhdCI6MTcwMTk0MzUzNiwiZXhwIjoxNzAyODA3NTM2LCJuYmYiOjE3MDE5NDM1MzYsImp0aSI6ImdvaDd2cTA4THZUYnh4VngiLCJzdWIiOjQyMDU4MjYsInBydiI6IjA1YmI2NjBmNjdjYWM3NDVmN2IzZGExZWVmMTk3MTk1YTIxMWU2ZDkifQ.RhPDlTJIGfZCUPr2mLy7QnoRdjizxQmI7wKHkpVEOy0'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        response_data = {
            "status": "true",
            "title": "Successfully Orderd",
            "message": "Order Created successfully.",
        }
        return JsonResponse(response_data)

