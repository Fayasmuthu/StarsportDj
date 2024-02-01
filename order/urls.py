from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    #wishlist
    path("shop/wishlist/", views.WishlistListView.as_view(), name="wishlist"),
    path("shop/wishlist/add/",views.AddToWishlistView.as_view(),name="add_to_wishlist"),
    path("shop/wishlist/remove/<int:product_id>/",views.RemoveFromWishlistView.as_view(),name="remove_from_wishlist"),
]
