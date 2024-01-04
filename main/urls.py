from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("dashboard/", views.IndexView.as_view(), name="index"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path("order/<str:order_id>/detail/", views.OrderDetailView.as_view(), name="order_detail"),
    path("order/update/", views.OrderUpdateView.as_view(), name="order_update"),
    # catgory
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/<str:pk>/update/", views.CategoryUpdate.as_view(), name="category_update"),
    path("category/<str:pk>/delete/", views.CategoryDelete.as_view(), name="category_delete"),
    # product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/create/", views.CreateProductView.as_view(), name="product_create"),
    path('product/<pk>/edit/', views.edit_product, name='product_update'),
    path("product/<str:pk>/delete/", views.ProductDelete.as_view(), name="product_delete"),
    # tag
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tag/<str:pk>/update/", views.TagUpdateView.as_view(), name="tag_update"),
    path("tag/<str:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    # state
    path("states/", views.StateListView.as_view(), name="states"),
    path("state/create/", views.StateCreateView.as_view(), name="state_create"),
    path("state/<str:pk>/update/", views.StateUpdateView.as_view(), name="state_update"),
    path("state/<str:pk>/delete/", views.StateDeleteView.as_view(), name="state_delete"),
     # district
    path("districts/", views.DistrictListView.as_view(), name="districts"),
    path("district/create/", views.DistrictCreateView.as_view(), name="district_create"),
    path("district/<str:pk>/update/", views.DistrictUpdateView.as_view(), name="district_update"),
    path("district/<str:pk>/delete/", views.DistrictDeleteView.as_view(), name="district_delete"),
    #customer
    path("customers/", views.CustomerListView.as_view(), name="customers"),
    
]
