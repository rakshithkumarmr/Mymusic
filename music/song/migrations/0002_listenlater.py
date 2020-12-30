# Generated by Django 2.2.13 on 2020-09-09 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('song', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listenlater',
            fields=[
                ('listen_id', models.AutoField(primary_key=True, serialize=False)),
                ('audio_id', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]