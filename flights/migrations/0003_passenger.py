# Generated by Django 4.2.2 on 2023-07-15 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0002_airport_alter_flight_destination_alter_flight_origin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=65)),
                ('last', models.CharField(max_length=65)),
                ('flights', models.ManyToManyField(blank=True, related_name='passengers', to='flights.flight')),
            ],
        ),
    ]
