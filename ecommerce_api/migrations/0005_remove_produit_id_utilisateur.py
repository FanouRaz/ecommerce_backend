# Generated by Django 4.2.2 on 2023-06-14 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_api', '0004_produit_id_utilisateur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='id_utilisateur',
        ),
    ]
