# Generated by Django 4.2.7 on 2024-01-24 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_review_fullname_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='approval',
            field=models.BooleanField(default=True),
        ),
    ]
