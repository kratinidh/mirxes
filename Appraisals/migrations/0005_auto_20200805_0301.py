# Generated by Django 3.0.6 on 2020-08-04 19:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appraisals', '0004_user_appraisal_list_mid_yearm_rejection'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_appraisal_list',
            name='bonusRecommendation',
            field=models.CharField(default='NIL', max_length=1000),
        ),
        migrations.AddField(
            model_name='user_appraisal_list',
            name='incrementRecommendation',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
