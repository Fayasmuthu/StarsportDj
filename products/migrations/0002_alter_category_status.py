# Generated by Django 5.0.1 on 2024-01-04 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('Published', 'Published'), ('Private', 'Private')], default='Published', max_length=100),
        ),
    ]
