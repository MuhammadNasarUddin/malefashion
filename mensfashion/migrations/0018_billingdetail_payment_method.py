# Generated by Django 5.0 on 2024-01-08 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensfashion', '0017_remove_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingdetail',
            name='payment_method',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
