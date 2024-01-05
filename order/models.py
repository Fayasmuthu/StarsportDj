import uuid
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.AvailableSize", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")

    def get_product_name(self):
        return self.product.name

    def get_total_price(self):
        return self.quantity * self.product.regular_price
    
    def cart_total(self):
        return float(sum(item.get_total_price() for item in CartItem.objects.filter(user=self.user)))

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.AvailableSize", on_delete=models.CASCADE)
    
    class Meta:
        # unique_together = ("user", "product")
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")

    def __str__(self):
        return f"{self.product.product.name}"
 

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"{self.title}"

def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]  # Generate a random 8-character string
    # yymm + unique_id upper
    return f"{timestamp}{unique_id.upper()}"

class Order(models.Model):
    unique_transaction_id = models.UUIDField(unique=True,  editable=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey("accounts.CustomerAddress", verbose_name="Shipping Address", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    item_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivered_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Placed"),
            ("Processing", "Confirmed"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ),
    )
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-id",)

    def save(self, *args, **kwargs):
        self.order_id = '#'+ generate_order_id()
        # Call the original save method
        super().save(*args, **kwargs)

    def get_updates(self):
        return OrderUpdate.objects.filter(order=self)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_payment(self):
        return Payment.objects.filter(order=self).last()
    def get_grand_total(self):
        total = self.item_subtotal + self.service_fee + self.shipping_fee
        return total
    def order_total(self):
        return float(sum([item.subtotal for item in self.get_items()]))
    
    def get_user_absolute_url(self):
        return reverse("accounts:order_detail", kwargs={"order_id": self.order_id})
    
    def __str__(self):
       return f"{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("products.AvailableSize", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.order} - {self.product}"

   
    def subtotal(self):
        return self.price * self.quantity


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,choices=(("COD","Cash On Delivery"),("OP","Online Payment")),default="COD")
    payment_id = models.CharField(max_length=50,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.order_id}"


