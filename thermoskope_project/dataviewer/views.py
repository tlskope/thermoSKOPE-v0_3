import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import CSVFile, CSVData
from plotly.offline import plot
from plotly.graph_objs import Scatter

def home_view(request):
    return render(request, 'dataviewer/home.html')

def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                handle_uploaded_file(file, user=request.user if request.user.is_authenticated else None)
                return render(request, 'dataviewer/upload_success.html')
            except KeyError as e:
                messages.error(request, f'Missing column in uploaded CSV: {e}')
                return redirect('dataviewer:upload_file')
    else:
        form = UploadFileForm()
    return render(request, 'dataviewer/upload.html', {'form': form})

def graph_view(request):
    # Placeholder for your actual data querying logic
    queryset = CSVData.objects.all()
    
    # Assuming 'x_value' is your x-axis and 'y_value' contains y-axis data
    x_data = [record.x_value for record in queryset]
    y_data = [record.y_value for record in queryset]  # Adjust based on how you want to use y_value

    # Create Plotly graph
    plot_div = plot([Scatter(x=x_data, y=y_data, mode='lines', name='Data Graph')],
                    output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    return render(request, 'dataviewer/graph.html', context={'plot_div': plot_div})

from django.utils.dateparse import parse_datetime



def handle_uploaded_file(file, user=None):
    csv_file_instance = CSVFile.objects.create(name=file.name, uploaded_by=user)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file)
    
    # Replace NaN values with None (which becomes 'null' in JSON)
    df.replace({np.nan: None}, inplace=True)

    # Iterate over the DataFrame and create CSVData instances
    for index, row in df.iterrows():
        x_value = str(row.iloc[0])  # Convert the first column to string
        y_value = row.iloc[1:].to_dict()  # Convert the remaining columns to a dictionary
        
        # Ensure y_value, now potentially containing None values, is saved correctly
        CSVData.objects.create(csv_file=csv_file_instance, x_value=x_value, y_value=y_value)
