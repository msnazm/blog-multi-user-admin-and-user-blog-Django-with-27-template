# Generated by Django 3.2.9 on 2021-12-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_alter_product_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='confirmed',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
