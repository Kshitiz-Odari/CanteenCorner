# Generated by Django 3.2.18 on 2023-05-17 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_items_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=200)),
            ],
        ),
    ]
