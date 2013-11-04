from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from api.handlers import BuildsHandler, BuildSetHandler, VersionSetHandler
ad = {}

builds_resource = Resource(handler=BuildsHandler, **ad)
buildSet_resource = Resource(handler=BuildSetHandler, **ad)
versionSet_resource = Resource(handler=VersionSetHandler, **ad)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^build/$', builds_resource),
    url(r'^build/(?P<build>[^/]+)/$', buildSet_resource),
    url(r'^build/(?P<build>[^/]+)/(?P<version>[^/]+)/$', versionSet_resource),
    url(r'^admin/', include(admin.site.urls)),
)
