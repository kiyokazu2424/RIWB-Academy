# Generated by Django 3.2 on 2022-09-12 00:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0003_alter_genre_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='text/'),
        ),
        migrations.AlterField(
            model_name='text',
            name='upload_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
