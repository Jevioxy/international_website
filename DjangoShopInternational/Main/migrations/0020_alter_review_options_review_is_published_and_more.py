# Generated by Django 4.2.2 on 2025-02-03 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0019_alter_actionhistory_model_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-creation_date'], 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AddField(
            model_name='review',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Опубликован'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=5, verbose_name='Рейтинг'),
        ),
    ]
