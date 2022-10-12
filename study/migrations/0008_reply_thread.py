# Generated by Django 3.2 on 2022-10-03 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('study', '0007_auto_20221003_0835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=32)),
                ('message', models.TextField(default='', max_length=200)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('text_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='study.text')),
                ('user_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='threads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reply', models.TextField(default='', max_length=200)),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('thread_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='study.thread')),
                ('user_id', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
