# Generated by Django 4.2.3 on 2023-12-09 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invention', '0018_rename_purchaseditems_purchaseditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dummy_count',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
