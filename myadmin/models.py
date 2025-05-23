from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
from authentication.models import CustomUser


class PowerPlant(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    admin = models.ManyToManyField(CustomUser, related_name='admins')
    drone_controller = models.ManyToManyField(
        CustomUser, related_name='drone_controllers')
    data_analyst = models.ManyToManyField(
        CustomUser, related_name='data_analysts')
    total_tasks = models.IntegerField()
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)

    class PowerPlantStatus(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'

    status = models.CharField(
        max_length=20,
        choices=PowerPlantStatus.choices,
        default=PowerPlantStatus.ACTIVE
    )

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    powerplant = models.ForeignKey(PowerPlant, on_delete=models.CASCADE, related_name="zone")
    # height and width meaning the number of row and column.
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return self.powerplant.name + ' - ' + self.name


class SolarCell(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="solar_cell")
    x_position = models.IntegerField()
    y_position = models.IntegerField() 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['zone', 'x_position', 'y_position'], name='unique_solarcell_position_per_zone')
        ]
    
    def __str__(self):
        return f"SolarCell at ({self.x_position}, {self.y_position}) in {self.zone.name}"


class Report(models.Model):
    powerplant = models.ForeignKey(
        PowerPlant, on_delete=models.CASCADE, related_name="report")
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    energy_generated = models.FloatField()

    def __str__(self):
        return f"{self.powerplant.name} Report #{self.id}"


class ReportResult(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="results")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report of {self.zone.name} when {self.report.createdAt} of {self.report}"

class CellEfficiency(models.Model):
    report_result = models.ForeignKey(ReportResult, on_delete=models.CASCADE, related_name="cell_efficiency")
    solar_cell = models.ForeignKey(SolarCell,on_delete=models.CASCADE, related_name="cell_efficiency")
    efficiency_percentage = models.FloatField()

    def __str__(self):
        return f"Cell of {self.solar_cell} for {self.report_result} "

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    powerplant = models.ForeignKey(PowerPlant, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.powerplant.name if self.powerplant else 'No PowerPlant'} - {self.zone.name if self.zone else 'No Zone'} - {self.uploaded_at.strftime('%Y-%m-%d')}"


