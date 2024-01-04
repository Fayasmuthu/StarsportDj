from django.contrib import admin

from .models import CartItem,Notification, Order, OrderItem, Payment, Wishlist

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class PaymentInline(admin.TabularInline):
    model = Payment
    max_num = 1
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'item_subtotal', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['order_id', 'user__username']
    inlines = [OrderItemInline, PaymentInline]

    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    pass
    # list_display = ("variant", "quantity")
    # search_fields = ("variant__product__title",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "description")
    search_fields = ("title",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    # list_display = ("user", "product")
    # search_fields = ("user__username", "product__name")
    pass