# Generated by Django 4.2.16 on 2024-11-08 03:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_stocks_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='high_price',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='stocks',
            name='last_fetched_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='stocks',
            name='low_price',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='stocks',
            name='returns',
            field=models.CharField(default='0.00%', max_length=100),
        ),
    ]
