# Generated by Django 5.0.6 on 2024-06-02 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('verbapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='irregularverb',
            unique_together={('base', 'past_simple', 'past_participle')},
        ),
    ]