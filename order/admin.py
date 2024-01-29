from django.contrib import admin

from .models import Order, OrderItem, Payment

# Register your models here.
class PaymentInline(admin.TabularInline):
    model = Payment
    max_num = 1
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id",'full_name','is_ordered', "payable", "order_status", "created",]
    list_filter = ["order_status", "created", "updated"]
    search_fields = ["order_id", "user__username"]
    inlines = (OrderItemInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request).all()
        return qs
admin.site.register(OrderItem)
    
# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     pass
#     # list_display = ("variant", "quantity")
#     # search_fields = ("variant__product__title",)


# @admin.register(Notification)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ("user", "title", "description")
#     search_fields = ("title",)


# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     # list_display = ("user", "product")
#     # search_fields = ("user__username", "product__name")
#     pass