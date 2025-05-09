from django.contrib import admin
from .models import PowerPlant, Zone, SolarCell, Report, ReportResult

admin.site.register(PowerPlant)
admin.site.register(Zone)
admin.site.register(SolarCell)
admin.site.register(Report)
admin.site.register(ReportResult)