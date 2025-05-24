# forms.py
from django import forms
from .models import ImageUpload, Zone, PowerPlant, Report

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']  # powerplant และ zone ใส่เองใน view

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['powerplant', 'energy_generated']
        widgets = {
            'powerplant': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'energy_generated': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full mt-4"})
    )
