# Generated by Django 4.2.2 on 2024-09-01 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_model_and_tochka_country_of_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model_and_tochka',
            name='name',
            field=models.CharField(default='Product', max_length=45, verbose_name='Название'),
        ),
    ]
