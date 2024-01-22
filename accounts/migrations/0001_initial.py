# Generated by Django 4.2.7 on 2024-01-22 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('Home', 'Home'), ('Work', 'Work')], default='Home', max_length=10)),
                ('full_name', models.CharField(max_length=100)),
                ('address_line_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address Line 2')),
                ('city', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=6)),
                ('mobile_no', models.CharField(max_length=15)),
                ('is_default', models.BooleanField(default=False, verbose_name='Set as Default')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.district')),
                ('state', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.state')),
            ],
            options={
                'verbose_name_plural': 'CustomerAddress',
            },
        ),
    ]
