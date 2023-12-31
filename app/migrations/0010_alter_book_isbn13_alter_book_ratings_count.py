# Generated by Django 4.1.1 on 2023-09-23 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_book_average_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn13',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='ratings_count',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
