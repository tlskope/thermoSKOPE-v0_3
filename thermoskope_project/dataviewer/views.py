import pandas as pd
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
    # Create a CSVFile instance
    csv_file_instance = CSVFile.objects.create(name=file.name, uploaded_by=user)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file)

    # Iterate over the DataFrame and create CSVData instances
    for index, row in df.iterrows():
        # Parse the first column as a datetime
        x_value = parse_datetime(row.iloc[0])
        if not x_value:
            # Handle cases where the date format is not automatically recognized
            # This will depend on the specific format of your date strings
            x_value = pd.to_datetime(row.iloc[0], format='%m/%d/%Y %I:%M %p')

        y_value = row.iloc[1:].to_dict()  # Remaining columns as y-values
        CSVData.objects.create(csv_file=csv_file_instance, x_value=x_value, y_value=y_value)
