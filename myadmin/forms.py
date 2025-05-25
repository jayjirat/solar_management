# forms.py
from django import forms
from .models import ImageUpload, Zone, PowerPlant, Report
from authentication.models import CustomUser
from django.db.models import Q

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
        print("USER:", user)
        print("HAS CUSTOM:", hasattr(user, 'custom'))
        custom_user = getattr(user, 'custom', None)

        if custom_user:
            self.fields['powerplant'].queryset = PowerPlant.objects.filter(
                Q(admin=custom_user) | Q(data_analyst=custom_user)
            ).distinct()
        else:
            print("ELSEEEEEE")
            self.fields['powerplant'].queryset = PowerPlant.objects.none()

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        widget=forms.FileInput(attrs={"class": "file-input file-input-bordered w-full mt-4"})
    )
