# Generated by Django 5.1.6 on 2025-05-08 05:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportresult',
            name='zone',
        ),
        migrations.AddField(
            model_name='reportresult',
            name='solar_cell',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='report_results', to='myadmin.solarcell'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportresult',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='myadmin.report'),
        ),
    ]
