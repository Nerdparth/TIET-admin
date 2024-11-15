from django.db import models

class Maintenance(models.Model):
    maintenance_mode = models.BooleanField(default=False)
