from django.db import models

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
    powerplant = models.ForeignKey(
        PowerPlant, on_delete=models.CASCADE, related_name="zone")
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return self.powerplant.name + ' - ' + self.name


class SolarCell(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="solar_cell")
    image = models.ImageField(upload_to='solarcell_images/', null=True, blank=True)

    def __str__(self):
        return f"SolarCell in {self.zone.name}"


class Report(models.Model):
    powerplant = models.ForeignKey(
        PowerPlant, on_delete=models.CASCADE, related_name="report")
    createdAt = models.DateField(auto_now_add=True)
    updatedAt = models.DateField(auto_now=True)
    energy_generated = models.FloatField()

    def __str__(self):
        return self.powerplant.name


class ReportResult(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="result")
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name="results")
    efficiency_percentage = models.FloatField()

    def __str__(self):
        return f"{self.zone.name} ({self.report.createdAt}) - {self.efficiency_percentage}%"

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    powerplant = models.ForeignKey(PowerPlant, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.powerplant.name if self.powerplant else 'No PowerPlant'} - {self.zone.name if self.zone else 'No Zone'} - {self.uploaded_at.strftime('%Y-%m-%d')}"


