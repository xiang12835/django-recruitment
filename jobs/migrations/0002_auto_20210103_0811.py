# Generated by Django 2.2.5 on 2021-01-03 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'verbose_name': '职位', 'verbose_name_plural': '职位列表'},
        ),
    ]
