# Generated by Django 4.0 on 2023-03-14 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('orders', '0008_remove_order_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('type', 1), ('type', 3), _connector='OR'), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders_from_driver', to='core.employee', verbose_name='Водитель'),
        ),
    ]
