from django.db import models


# Create your models here.
class ModelFile(models.Model):
  image = models.ImageField(upload_to='documents/')
  label = models.CharField(max_length=120, null=True)
  proba = models.FloatField(null=True)
