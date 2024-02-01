

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
import requests
from products.models import AvailableSize
from order.models import OrderItem, Payment, Wishlist,Order
from accounts.models import CustomerAddress

# CART
from web.cart import Cart


#wishlist
class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        cart_instance = cart.cart
        wishlist_count = Wishlist.objects.filter(user=self.request.user).count()
        context["wishlist_count"] = wishlist_count
        context["cart_count"] = len(cart_instance)
        return context


class AddToWishlistView( View):
    def get(self, request ):
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
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            return JsonResponse({'message': 'Product Added from Wishlist successfully',
                                 'wishlist_count': wishlist_count})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.'})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        return JsonResponse({'message': 'Product Removed from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})

