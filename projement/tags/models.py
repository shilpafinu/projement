from django.db import models
from projects.views import Project

# Create your models here.


class Tag(models.Model):

    class Meta:
        verbose_name_plural = "tags"

    name = models.CharField(max_length=16)
    project = models.ManyToManyField(Project)

    def __str__(self):
        return self.name

