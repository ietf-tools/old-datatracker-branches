# Copyright The IETF Trust 2021 All Rights Reserved
# Generated by Django 2.2.19 on 2021-04-02 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('group', '0044_populate_groupfeatures_parent_type_fields'),
        ('name', '0029_populate_agendafiltertypename'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupfeatures',
            name='agenda_filter_type',
            field=models.ForeignKey(default='none', on_delete=django.db.models.deletion.PROTECT,
                                    to='name.AgendaFilterTypeName'),
        ),
    ]
