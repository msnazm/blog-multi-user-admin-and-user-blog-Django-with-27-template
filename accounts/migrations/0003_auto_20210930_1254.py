# Generated by Django 3.2 on 2021-09-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_verificationuser_verification_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationuser',
            name='user',
        ),
        migrations.AddField(
            model_name='verificationuser',
            name='user_email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verificationuser',
            name='verification_code',
            field=models.IntegerField(),
        ),
    ]
