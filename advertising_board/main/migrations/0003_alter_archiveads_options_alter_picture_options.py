# Generated by Django 4.0.3 on 2022-03-30 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_archiveads_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='archiveads',
            options={},
        ),
        migrations.AlterModelOptions(
            name='picture',
            options={'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
    ]
