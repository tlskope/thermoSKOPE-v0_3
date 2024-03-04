from django.db import migrations, models
import datetime

def forward_convert_x_value(apps, schema_editor):
    CSVData = apps.get_model('dataviewer', 'CSVData')
    for row in CSVData.objects.all():
        # Assuming the original x_value field contains a UNIX timestamp (float) and needs conversion
        # This is an example conversion; adjust the logic to fit your actual data format and requirements
        # For instance, if x_value contains a string that represents a datetime, you'll parse it differently
        timestamp = row.x_value
        converted_datetime = datetime.datetime.fromtimestamp(timestamp)
        row.x_value_temp = converted_datetime
        row.save(update_fields=['x_value_temp'])

def backward_convert_x_value(apps, schema_editor):
    # This function would convert data back if needed; for many use cases, this might be left empty
    pass
class Migration(migrations.Migration):

    dependencies = [
        ('dataviewer', '0004_rename_x_value_csvdata_x_value_temp'),
    ]

    operations = [
        migrations.RunPython(forward_convert_x_value, backward_convert_x_value),
    ]
