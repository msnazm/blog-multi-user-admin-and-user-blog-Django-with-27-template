# Generated by Django 3.2.9 on 2021-12-10 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_product_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='confirmed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
