# Generated by Django 5.0.2 on 2024-03-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_picture',
            field=models.ImageField(blank=True, default='book_image/default_book.png', null=True, upload_to='book_image/'),
        ),
    ]
