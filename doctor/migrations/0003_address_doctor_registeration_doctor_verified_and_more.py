# Generated by Django 4.0.2 on 2022-05-08 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_remove_doctor_specialization_doctor_specialization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('house_flat_no', models.CharField(max_length=50)),
                ('locality', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='registeration',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='address_doctor', to='doctor.address'),
        ),
    ]
