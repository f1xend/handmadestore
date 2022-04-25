# Generated by Django 3.2.2 on 2021-05-16 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210514_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_category', to='main.category', verbose_name='Главная категория'),
        ),
    ]
