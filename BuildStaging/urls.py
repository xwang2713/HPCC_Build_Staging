from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^staging/Local/', include('LocalStageListing.urls')),
    url(r'^staging/api/', include('api.urls')),
)

#urlpatterns += staticfiles_urlpatterns()
