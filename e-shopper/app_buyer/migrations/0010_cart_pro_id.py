# Generated by Django 4.2.1 on 2023-07-20 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller_buyer', '0003_product'),
        ('app_buyer', '0009_remove_cart_pro_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='pro_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller_buyer.product'),
        ),
    ]