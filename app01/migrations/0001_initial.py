# Generated by Django 3.2 on 2022-02-25 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='title')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='name')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
                ('age', models.IntegerField(verbose_name='age')),
                ('account', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='account')),
                ('create_time', models.DateTimeField(verbose_name='time')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='sex')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.department', verbose_name='部门')),
            ],
        ),
    ]
