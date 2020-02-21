# Generated by Django 3.0.3 on 2020-02-21 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchangehistory',
            old_name='from_data',
            new_name='from_date',
        ),
        migrations.RenameField(
            model_name='exchangehistory',
            old_name='until_data',
            new_name='until_date',
        ),
        migrations.AlterUniqueTogether(
            name='exchangehistory',
            unique_together={('currency', 'from_date')},
        ),
    ]