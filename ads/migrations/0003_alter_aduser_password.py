# Generated by Django 4.0.1 on 2023-01-10 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_aduser_first_name_alter_location_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aduser',
            name='password',
            field=models.SlugField(max_length=128),
        ),
    ]
