# Generated by Django 4.1.1 on 2023-09-20 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookID', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('authors', models.CharField(max_length=200)),
                ('average_ratings', models.FloatField(blank=True)),
                ('isbn', models.IntegerField()),
                ('isbn13', models.IntegerField()),
                ('language_code', models.CharField(max_length=10)),
                ('num_pages', models.PositiveIntegerField(blank=True)),
                ('ratings_count', models.PositiveIntegerField(blank=True)),
                ('text_reviews_count', models.IntegerField(blank=True)),
                ('publication_on_date', models.DateField()),
                ('publisher', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=10)),
                ('isbn', models.CharField(max_length=50)),
                ('amount_paid', models.IntegerField()),
                ('amount_remaining', models.IntegerField()),
                ('issued_date', models.DateField(auto_now=True)),
                ('return_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]