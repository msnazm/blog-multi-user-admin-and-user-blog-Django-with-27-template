# Generated by Django 3.2.9 on 2021-12-24 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20211224_1013'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageone', models.ImageField(blank=True, upload_to='images/%Y/%m/%d')),
                ('name', models.CharField(max_length=255)),
                ('datecreate', models.CharField(max_length=50)),
                ('datecreatealt', models.BigIntegerField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.store')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
