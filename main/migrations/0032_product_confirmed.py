# Generated by Django 3.2.9 on 2021-12-10 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_userstore_agree'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='confirmed',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
