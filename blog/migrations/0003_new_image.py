# Generated by Django 5.1 on 2024-10-25 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_new_options_alter_new_author_alter_new_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='image',
            field=models.ImageField(null=True, upload_to='images', verbose_name='Картинка'),
        ),
    ]