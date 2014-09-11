from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import medical_eponyms.urls


urlpatterns = patterns('',
    url(r'^eponyms/', include(medical_eponyms.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
