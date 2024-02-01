# Generated by Django 4.2.7 on 2024-02-01 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_transaction_id', models.UUIDField(blank=True, editable=False, null=True, unique=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('payable', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_id', models.CharField(default=order.models.generate_order_id, max_length=255)),
                ('is_ordered', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('COD', 'Cash On Delivery'), ('OP', 'Online Payment')], default='COD', max_length=20)),
                ('full_name', models.CharField(max_length=100)),
                ('address_line_1', models.CharField(max_length=100, verbose_name='Complete Address')),
                ('address_line_2', models.CharField(max_length=100, verbose_name='Landmark')),
                ('state', models.CharField(max_length=200, null=True)),
                ('district', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=100)),
                ('pin_code', models.IntegerField()),
                ('mobile_no', models.CharField(max_length=15)),
                ('alternative_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Placed', 'Order Placed'), ('Shipped', 'Order Shipped'), ('InTransit', 'In Transit'), ('Delivered', 'Order Delivered'), ('Cancelled', 'Order Cancelled')], default='Pending', max_length=50)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Success', 'Success'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.availablesize')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wishlist Item',
                'verbose_name_plural': 'Wishlist Items',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('COD', 'Cash On Delivery'), ('OP', 'Online Payment')], default='COD', max_length=20)),
                ('payment_id', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.availablesize')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
