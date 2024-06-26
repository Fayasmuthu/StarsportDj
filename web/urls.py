from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "web"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", TemplateView.as_view(template_name="web/about.html"), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    # policy
    path("privacy-policy/",TemplateView.as_view(template_name="web/privacy_policy.html"),name="privacy_policy"),
    path("terms-conditions/",TemplateView.as_view(template_name="web/terms_conditions.html"),name="terms_conditions"),
    path("refund-policy/",TemplateView.as_view(template_name="web/refund_policy.html"),name="refund_policy"),
    path("shipping-policy/", TemplateView.as_view(template_name="web/shipping_policy.html"),name="shipping_policy"),
    # shop
    path("shop/", views.ShopView.as_view(), name="shop"),
    path("product-detail/<slug:slug>/",views.ProductDetailView.as_view(),name="product_detail"),
    path("offered-products/<int:offer_id>/",views.OfferedProductListView.as_view(),name="offered_product_list"),
    path('product/filter-data',views.filter_data, name="filter-data"),
    path('product/filter-range-price',views.filter_range_price, name="filter-range-price"),

    #checkout
    path("whatsapp-order/", views.order, name="order"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("get_shipping_fee/", views.get_shipping_fee, name="get_shipping_fee"),
    # CART
    path("shop/cart/", views.cart_view, name="cart"),
    path("shop/cart/add/", views.cart_add, name="add_cart"),
    path("shop/cart-item-clear/<str:item_id>/",views.clear_cart_item,name="clear_cart_item"),
    path("shop/cart-minus/", views.minus_to_cart, name="minus_to_cart"),
    path("shop/cart-clear/", views.clear_cart, name="clear_cart"),

    # payment
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("callback/<str:pk>/", views.callback, name="callback"),
    path(
        "complete-order/<str:pk>/",
        views.CompleteOrderView.as_view(),
        name="complete_order",
    ),
    path(
        "user/order/<str:order_id>/detail/",
        views.UserOrderDetailView.as_view(),
        name="order_detail",
    ),
    # path(
    #     "offer-detail/<pk>/",
    #     views.OfferDetailView.as_view(),
    #     name="offer_details",
    # ),
]


