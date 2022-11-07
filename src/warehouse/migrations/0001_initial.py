# Generated by Django 4.0 on 2022-11-06 08:47

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_alter_customgroup_options_alter_customuser_groups_and_more'),
        ('orders', '0002_order_user'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('document_number', models.CharField(blank=True, max_length=64, verbose_name='Номер документа')),
                ('provider', models.CharField(blank=True, max_length=128, verbose_name='Поставщик')),
                ('note', models.TextField(blank=True, verbose_name='Примечание')),
                ('responsible', models.ForeignKey(limit_choices_to={'type': 3}, on_delete=django.db.models.deletion.PROTECT, related_name='enrance_from_responsible', to='core.employee', verbose_name='Кто оприходовал')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='entrances', to='authentication.customuser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Поступление',
                'verbose_name_plural': 'Поступления',
                'ordering': ('-date', '-pk'),
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Наименование')),
                ('article_number', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Код (Артикул)')),
                ('compatbility', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), blank=True, size=None, verbose_name='Cовместимость c ТС')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Категория материалов',
                'verbose_name_plural': 'Категории материалов',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Наименование')),
                ('is_precision_point', models.BooleanField(default=False, help_text='Отметьте, если для измерения количества требуется точность с плавающей запятой.', verbose_name='Число с плавающей запятой')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Turnover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'Приход'), (2, 'Расход')], verbose_name='Тип')),
                ('date', models.DateField(verbose_name='Дата')),
                ('is_correction', models.BooleanField(default=False, verbose_name='Корректировка')),
                ('note', models.TextField(blank=True, verbose_name='Примечание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Количество')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма')),
                ('entrance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='turnovers_from_entrance', to='warehouse.entrance', verbose_name='Приход')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turnovers', to='warehouse.material', verbose_name='Материал')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='turnovers_from_order', to='orders.order', verbose_name='Заказ-наряд')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turnover', to='authentication.customuser', verbose_name='Пользователь')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turnovers', to='warehouse.warehouse', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Движение материала',
                'verbose_name_plural': 'Движение материалов',
                'ordering': ('date', 'pk'),
            },
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='warehouse.materialcategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='material',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='warehouse.unit', verbose_name='Единица измерения'),
        ),
    ]