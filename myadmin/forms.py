# forms.py
from django import forms
from .models import ImageUpload, ReportResult, CellEfficiency

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']  # powerplant และ zone ใส่เองใน view

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
