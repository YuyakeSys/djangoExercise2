# Generated by Django 3.2 on 2022-03-01 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_prettynum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name='username')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
            ],
        ),
    ]
