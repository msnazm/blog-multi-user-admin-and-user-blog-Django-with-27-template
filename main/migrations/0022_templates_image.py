# Generated by Django 3.2.9 on 2021-12-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_templates'),
    ]

    operations = [
        migrations.AddField(
            model_name='templates',
            name='image',
            field=models.ImageField(blank=True, upload_to='image/'),
        ),
    ]
