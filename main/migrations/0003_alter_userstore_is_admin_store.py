# Generated by Django 3.2.9 on 2021-11-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_userstore_store_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstore',
            name='is_admin_store',
            field=models.BooleanField(default=True),
        ),
    ]
