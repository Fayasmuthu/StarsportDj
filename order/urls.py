from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    #cart
    path("shop/cart/", views.CartView.as_view(), name="cart"),
    path("shop/cart/add/", views.AddToCartView.as_view(), name="add_to_cart"),
    path('shop/cart/minus/', views.MinusCartView.as_view(), name='minus_to_cart'),
    path("shop/cart/remove/<int:cart_item_id>/",views.RemoveCartItemView.as_view(),name="remove_cart_item"),
    path('shop/clear-cart/', views.ClearCartView.as_view(), name='clear_cart'),
    #wishlist
    path("shop/wishlist/", views.WishlistListView.as_view(), name="wishlist"),
    path("shop/wishlist/add/",views.AddToWishlistView.as_view(),name="add_to_wishlist"),
    path("shop/wishlist/remove/<int:product_id>/",views.RemoveFromWishlistView.as_view(),name="remove_from_wishlist"),
    #checkout
    path("shop/checkout/", views.CheckoutView.as_view(), name="checkout"),
    #orders
    path("shop/order/create/", views.OrderCreateView.as_view(), name="order_create"),
    
]
