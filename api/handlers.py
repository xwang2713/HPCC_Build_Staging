import re

from django.conf import settings

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from models import HPCCBuilds

import sys

# This only executs when web app starts
# If there is new projects created after it
# reference these projects from URL will fail
#buildObj = HPCCBuilds(settings.BUILD_DIR)

class BuildsHandler(BaseHandler):
    allowed_methods = {'GET'}

    def read(self, request):
        buildObj = HPCCBuilds(settings.BUILD_DIR)
        return {"builds": buildObj.builds}

class BuildSetHandler(BaseHandler):
    allowed_methods = {'GET'}
    fields = ('build')

    def read(self, request, build):
        buildObj = HPCCBuilds(settings.BUILD_DIR)
        if not build in buildObj.builds:
            return resError(5001, "Bad build name.")

        bS = buildObj.getBuildSets(build)	
        return {'buildSet': bS.versions}

class VersionSetHandler(BaseHandler):
    allowed_methods = {'GET'}
    fields = ('build', 'version')

    def read(self, request, build, version):
        buildObj = HPCCBuilds(settings.BUILD_DIR)
    	version_dict = {}
    	if not build in buildObj.builds:
            return resError(5001, "Bad build name.")
        
        bS = buildObj.getBuildSets(build)

        if not version in bS.versions:
            return resError(request, 5002, "Bad version number.")
        vS = bS.getVersionSets(version)
        version_dict.update({'Version':version})
        version_dict.update({'Major':vS.versionParts['Major']})
        version_dict.update({'Minor':vS.versionParts['Minor']})
        version_dict.update({'Point':vS.versionParts['Point']})
        version_dict.update({'Sequence':vS.versionParts['Sequence']})
        version_dict.update({'type':vS.versionParts['type']})
        
        files = []
        for file in vS.files:
            try:
                link = file.osTemplate['link']
                vm_arch = ''
                if "VM" in file.osTemplate['id']:
                    link = file.osTemplate['link'] + file.version
                    if file.file.find('amd64') >= 0:
                        vm_arch = ' 64bit'
                    else:
                        vm_arch = ' 32bit'
                files.append({
            	    'Type': file.install,
            	    'OS': file.osTemplate['name'],
            	    'Version_Number': file.version,
            	    'File_Name': file.file,
            	    'MD5': file.md5,
            	    'Edge_Cast_Path': 'releases'+file.getRelativePath(settings.BUILD_DIR),
            	    'Download_Size': file.size,
            	    'Display_Name': file.osTemplate['title']  + vm_arch,
            	    'Link_Text': file.osTemplate['text'],
            	    'Link_Path': link
                })
            except:
                pass
        version_dict.update({'files':files})
        return version_dict
