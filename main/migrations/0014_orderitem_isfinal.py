# Generated by Django 3.2.9 on 2021-11-25 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20211125_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='isfinal',
            field=models.BooleanField(default=False),
        ),
    ]
