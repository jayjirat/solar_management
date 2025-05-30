# Generated by Django 5.1.6 on 2025-05-09 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_solarcell_x_zposition_solarcell_y_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportresult',
            name='zone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myadmin.zone'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reportresult',
            name='solar_cell',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.solarcell'),
        ),
    ]
