# Generated by Django 4.2.7 on 2024-02-07 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderitem_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='image',
        ),
    ]
