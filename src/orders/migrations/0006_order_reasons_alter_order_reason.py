# Generated by Django 4.0 on 2023-02-08 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='reasons',
            field=models.ManyToManyField(related_name='orders', to='orders.Reason', verbose_name='Причины'),
        ),
        migrations.AlterField(
            model_name='order',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='orders.reason', verbose_name='Причина'),
        ),
    ]
