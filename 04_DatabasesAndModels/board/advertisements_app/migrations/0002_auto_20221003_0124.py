# Generated by Django 2.2 on 2022-10-02 22:24

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertisementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adv_type', models.CharField(max_length=100, verbose_name='Тип объявления')),
            ],
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='date_cancel',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 1, 22, 24, 20, 699800, tzinfo=utc), verbose_name='Дата окончания публикации'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='adv_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='advertisements_app.AdvertisementType', verbose_name='Тип объявления'),
        ),
    ]
