from django.contrib import admin
from .models import PowerPlant, Zone, SolarCell, Report, ReportResult, ImageUpload, CellEfficiency

admin.site.register(PowerPlant)
admin.site.register(Zone)
admin.site.register(SolarCell)
admin.site.register(Report)
admin.site.register(ReportResult)
admin.site.register(ImageUpload)
admin.site.register(CellEfficiency)