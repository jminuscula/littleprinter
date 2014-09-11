from django.conf.urls import patterns, include, url

import django.views.static
from medical_eponyms.views import Edition, Sample, ValidateConfig


urlpatterns = patterns('',
    url(r'^edition/', Edition.as_view(), name="edition"),
    url(r'^sample/', Sample.as_view(), name="sample"),
    url(r'^validate_config/', ValidateConfig.as_view(), name="validate_config"),

    # statics
    url(r'^meta.json', django.views.static.serve,
        {"path": "static/meta.json", "document_root": "medical_eponyms"},
        name="meta"),
    url(r'^icon.png', django.views.static.serve,
        {"path": "static/icon.png", "document_root": "medical_eponyms"},
        name="icon"),
)
