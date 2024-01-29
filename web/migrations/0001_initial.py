# Generated by Django 4.2.7 on 2024-01-29 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('place', models.CharField(max_length=120)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
