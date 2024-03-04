from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('dataviewer', '0005_auto_20240305_0933'),  # Update this to your actual last migration before this one
    ]

    operations = [
        # Step A: Add a new temporary column for datetime data
        migrations.AddField(
            model_name='csvdata',
            name='x_value_temp',
            field=models.DateTimeField(null=True),
        ),
        # Assuming manual data conversion is handled outside of Django migrations,
        # for example, through a script or manually in the database.
        
        # Step B: Remove the original x_value column (this step may need to be adjusted based on actual data handling)
        migrations.RemoveField(
            model_name='csvdata',
            name='x_value',
        ),
        
        # Step C: Rename the new temporary column back to x_value
        migrations.RenameField(
            model_name='csvdata',
            old_name='x_value_temp',
            new_name='x_value',
        ),
    ]
