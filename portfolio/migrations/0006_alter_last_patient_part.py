# Generated by Django 3.2.5 on 2021-07-12 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_csv_file_data_model_department_model_detailed_file_uploaded_file_details_uploading_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='last_patient',
            name='part',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.body_part'),
        ),
    ]
