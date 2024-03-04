import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
import plotly.graph_objs as go
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
    queryset = CSVData.objects.all()

    fig = go.Figure()

    # Assuming x_value is the same for all and represents some sort of timestamp or category
    x_data = queryset.first().x_value  # This needs to be adjusted based on your actual data structure

    for csv_data_instance in queryset:
        # Assuming csv_data_instance.y_value is a dictionary where each key is a variable name and each value is its corresponding value
        for key, value in csv_data_instance.y_value.items():
            # Here, you might need to handle None values or convert them to a numeric type that Plotly can handle (e.g., 0 or np.nan)
            # This example assumes all values are already appropriate for plotting
            fig.add_trace(go.Scatter(x=[x_data], y=[value], mode='lines', name=key))

    # Convert Plotly figure to HTML div
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    return render(request, 'dataviewer/graph.html', context={'plot_div': plot_div})



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
