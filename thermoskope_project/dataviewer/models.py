from django.db import models
from django.contrib.auth.models import User  # Optional: if you want to track who uploaded the file

class DataRecord(models.Model):
    # Example fields based on your CSV structure
    # You should modify these fields according to the actual structure of your CSV
    field1 = models.CharField(max_length=200)
    field2 = models.FloatField()
    # Add more fields as necessary

class CSVFile(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional

    def __str__(self):
        return self.name

class CSVData(models.Model):
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE, related_name='data')
    x_value_temp = models.DateTimeField()  # Temporary new field for datetime values
    y_value = models.JSONField()

    def __str__(self):
        return f"Data for {self.csv_file.name} - X Value: {self.x_value}"
