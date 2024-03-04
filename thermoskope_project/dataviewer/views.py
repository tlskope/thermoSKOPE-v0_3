import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm
from .models import DataRecord
from plotly.offline import plot
from plotly.graph_objs import Scatter
from .models import CSVFile, CSVData

def home_view(request):
    return render(request, 'home.html')

def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                # Create DataRecord instance for each row and save to database
                # Adjust field names based on your CSV structure and model
                DataRecord.objects.create(field1=row['ColumnName1'], field2=row['ColumnName2'])
            return render(request, 'dataviewer/upload_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'dataviewer/upload.html', {'form': form})

def graph_view(request):
    # Query your model for data
    # This is a placeholder; adjust according to your model and data structure
    queryset = DataRecord.objects.all()
    
    # Assuming 'field1' is your x-axis and 'field2' is your y-axis
    x_data = [record.field1 for record in queryset]
    y_data = [record.field2 for record in queryset]

    # Create Plotly graph
    plot_div = plot([Scatter(x=x_data, y=y_data, mode='lines', name='Test Graph')],
                    output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    return render(request, 'dataviewer/graph.html', context={'plot_div': plot_div})

def handle_uploaded_file(file, user=None):
    # Create a CSVFile instance
    csv_file_instance = CSVFile.objects.create(name=file.name, uploaded_by=user)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file)

    # Iterate over the DataFrame and create CSVData instances
    for index, row in df.iterrows():
        x_value = row.iloc[0]  # First column as x-value
        y_value = row.iloc[1:].to_dict()  # Remaining columns as y-values
        CSVData.objects.create(csv_file=csv_file_instance, x_value=x_value, y_value=y_value)

