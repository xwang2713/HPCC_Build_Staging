from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^Stage/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.BUILD_DIR, 'show_indexes': True}),
    url(r'^$', 'LocalStageListing.views.index')
)
