# Generated by Django 5.0 on 2024-01-08 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensfashion', '0015_billingdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingdetail',
            name='notes',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
