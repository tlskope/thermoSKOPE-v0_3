# Generated by Django 5.0.3 on 2024-03-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataviewer', '0002_csvfile_csvdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdata',
            name='x_value',
            field=models.DateTimeField(),
        ),
    ]
