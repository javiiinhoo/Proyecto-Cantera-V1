# Generated by Django 4.1.7 on 2023-03-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_configuracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='aprobado',
            field=models.BooleanField(default=False),
        ),
    ]
