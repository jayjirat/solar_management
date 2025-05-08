# forms.py
from django import forms
from .models import SolarCell

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = SolarCell
        fields = ['zone', 'image']
