# Generated by Django 3.2.12 on 2022-03-20 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetparticipant',
            name='can_add_components',
        ),
    ]