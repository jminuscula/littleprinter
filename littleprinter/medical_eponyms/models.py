from django.db import models


class MedicalEponym(models.Model):
    name = models.CharField(max_length=512)
    title = models.CharField(max_length=512)
    summary = models.TextField()
    order = models.IntegerField()

    @property
    def altname(self):
        return self.title.lower() != self.name.lower()

    class Meta:
        ordering = ('order', )

    def __str__(self):
        return self.name
