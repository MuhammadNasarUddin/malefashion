# Generated by Django 5.0 on 2024-01-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mensfashion', '0021_alter_order_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='user',
            new_name='email',
        ),
    ]