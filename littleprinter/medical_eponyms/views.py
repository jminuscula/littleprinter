import random
from datetime import datetime

from django.http import Http404
from django.core.exceptions import SuspiciousOperation
from django.views.generic import TemplateView

from medical_eponyms.models import MedicalEponym


class Edition(TemplateView):
    template_name = "medical_eponyms/edition.html"

    def _get_delivery_day(self, post):
        tm = post.get("local_delivery_time")
        try:
            # remove timezone from 2013-11-18T23:20:30-08:00
            date = datetime.strptime(tm[:19], "%Y-%m-%dT%H:%M:%S")
            return date.timetuple().tm_yday - 1  # Jan 1st is day 1
        except (TypeError, ValueError):
            return None

    def get_context_data(self, **kwargs):
        day = self._get_delivery_day(self.request.POST)
        if day is None:
            raise SuspiciousOperation("Unrecognized date format")

        total = MedicalEponym.objects.count()
        if total == 0:
            raise Http404

        eponym = MedicalEponym.objects.get(order=day % total)
        return {
            "eponym": eponym,
            "publication_name": "Medical Eponyms"
        }


class Sample(TemplateView):
    template_name = "medical_eponyms/edition.html"

    def get_context_data(self, **kwargs):
        return {
            "eponym": MedicalEponym.objects.get(order=0),
            "publication_name": "Medical Eponyms"
        }

class ValidateConfig(TemplateView):
    pass
