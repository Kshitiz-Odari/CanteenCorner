# Generated by Django 3.2.18 on 2023-06-13 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_alter_staff_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='items',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.items'),
        ),
    ]
