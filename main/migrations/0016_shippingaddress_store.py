# Generated by Django 3.2.9 on 2021-11-27 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_shippingaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.store'),
        ),
    ]