# Generated by Django 3.0.14 on 2021-05-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_app', '0006_bodyweight_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodyweight',
            name='weight',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
