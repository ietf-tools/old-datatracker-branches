# Copyright The IETF Trust 2019-2020, All Rights Reserved
# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-09 05:46


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0016_set_document_docalias_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docalias',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
