from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("user/address/add/", views.AddAddress.as_view(), name="address_create"),
    path("user/address/get/", views.get_address_data, name="address_get"),
    path('user/address/<int:pk>/edit/', views.customer_address_edit, name='address_update'),
    path("user/address/<int:pk>/delete/", views.delete_address, name="address_delete"),
    path("user/address/", views.AddressListView.as_view(), name="address_list"),
    #order
    path("user/orders/", views.UserOrderListView.as_view(), name="orders"),
    path("user/order/<str:order_id>/detail/", views.UserOrderDetailView.as_view(), name="order_detail"),
    #setting
    path("user/setting/", views.SettingView.as_view(), name="setting"),
]
