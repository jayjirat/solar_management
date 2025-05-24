# forms.py
from django import forms
from .models import ImageUpload, Zone, PowerPlant, Report
from authentication import models
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 🔹 Grab the user from kwargs
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'custom'):
            self.fields['powerplant'].queryset = PowerPlant.objects.filter(
                models.Q(admin=user.custom) | models.Q(data_analyst=user.custom)
            ).distinct()
        else:
            self.fields['powerplant'].queryset = PowerPlant.objects.none()  # No access

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full mt-4"})
    )
