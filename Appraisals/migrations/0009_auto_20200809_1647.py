# Generated by Django 3.0.6 on 2020-08-09 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appraisals', '0008_auto_20200809_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peerappraisal',
            name='strength1',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='peerappraisal',
            name='strength2',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='peerappraisal',
            name='strength3',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='peerappraisal',
            name='weaknessdevelopment1',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='peerappraisal',
            name='weaknessdevelopment2',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='peerappraisal',
            name='weaknessdevelopment3',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
