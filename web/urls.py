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

]
