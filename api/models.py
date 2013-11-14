import fnmatch
import hashlib
import os
import re
import sys

from django.conf import settings
from django.db import models
from django.utils import simplejson
import json

OS = settings.OS
EXT = settings.EXT
BUILD_PATHS = settings.BUILD_PATHS
OPT_BUILD_PATHS = settings.OPT_BUILD_PATHS
VERSION_RE = settings.VERSION_RE
VERSION_RE_NORMALIZED = settings.VERSION_RE_NORMALIZED


def uniq(seq):
    uList = set(seq)
    return [item for item in seq if item in uList and not uList.remove(item)]


class Os(models.Model):
    os = models.CharField('OS', max_length=30, unique=True)
    name = models.CharField('OS Name', max_length=30, unique=True)

    def __unicode__(self):
        return self.os

class install(models.Model):
    type = models.CharField('File Type',max_length=30)

    def __unicode__(self):
        return self.type

class OsTemplate2(models.Model):
    Tos = models.ForeignKey(Os, verbose_name='OS', related_name='Tos', to_field='os')
    Tid = models.CharField('Id', max_length=30)
    Tname = models.ForeignKey(Os, verbose_name='OS Name', related_name='Tname', to_field='name')
    Tinstall = models.ForeignKey(install, verbose_name='File Type')
    Ttitle = models.CharField('Title', max_length=80)
    Ttext = models.CharField('Link Text', max_length=256)
    Tlink = models.CharField('Link Path', max_length=256)

    def __unicode__(self):
        return self.Tos

class OsTemplate(models.Model):
    Tos = models.CharField('OS', max_length=30)
    Tid = models.CharField('Id', max_length=30)
    Tname = models.CharField('OS Name', max_length=30)
    Tinstall = models.CharField('File Type', max_length=30)
    Ttitle = models.CharField('Title', max_length=80)
    Ttext = models.CharField('Link Text', max_length=256)
    Tlink = models.CharField('Link Path', max_length=256)

    def __unicode__(self):
        return self.Tos

class HPCCError(Exception):

    def __init__(self, errno, strerror):
        self.errno = errno
        self.strerror = strerror

    def __str__(self):
        error = "Error ({0}): {1}".format(self.errno, self.strerror)
        return repr(error)
    
    def __repr__(self):
        return simplejson.dumps(self.__dict__)


class HPCCBase(object):
    def __init__(self):
        pass

    def genBuildDirs(self, path, opts=False):
        dirs = list()
        for bPath in BUILD_PATHS:
            dirs.append(os.path.join(path, bPath))
        if opts:
            for bPath in OPT_BUILD_PATHS:
                dirs.append(os.path.join(path, bPath))
        return dirs

    def get_ver_string(self, file):
        p = re.compile(VERSION_RE_NORMALIZED)
        s = p.search(file)
        try:
            return s.group()
        except:
            np = re.compile(VERSION_RE)
	    ns = np.search(file)
            try:
                return '-'.join(ns.group().rsplit('.', 1))
            except:
                raise HPCCError(1001,
                    "Cannot get version: {0}".format(file)
                )
        return False

    def get_ver_dict(self, version):
        p = re.compile(VERSION_RE)
        s = p.search(version)
        ver_dict = {}
        try:
            vG = s.groups()
            ver_dict.update({'Major':vG[0]})
            ver_dict.update({'Minor':vG[1]})
            ver_dict.update({'Point':vG[2]})
            if vG[5]:
                ver_dict.update({'type':vG[4]})
		ver_dict.update({'Sequence':vG[5]})
            else:
                ver_dict.update({'type':'release'})
		ver_dict.update({'Sequence':vG[4]})
            return ver_dict
        except:
            raise HPCCError(1001,
            	    "Cannot get version: {0}".format(version)
            	)
        return False

    def cmp_ver(self, ver_string, file):
        ver = self.get_ver_string(file)
        if ver == ver_string:
            return True
        return False

    def filter_list_by_extension(self, file, alist_filter=EXT):
        if file.endswith(tuple(alist_filter)) or len(alist_filter) == 0:
            return True
        return False

    def get_file_list(self, build, ver=False):
        files = list()
        dirs = self.genBuildDirs(build, True)
        for dir in dirs:
            if os.path.isdir(dir):
                for file in os.listdir(dir):
                    if self.filter_list_by_extension(file):
                        if ver and self.cmp_ver(ver, file):
                            rawFile = os.path.join(dir, file)
                            files.append(rawFile)
        return files

    def get_ver_list(self, build):
        ver_list = list()
        dirs = self.genBuildDirs(build, True)
        for dir in dirs:
            if os.path.isdir(dir):
                for file in os.listdir(dir):
                    if self.filter_list_by_extension(file):
                        ver = self.get_ver_string(file)
                        if not ver in ver_list:
                            ver_list.append(ver)
        return ver_list

    def checkDirs(self, dirs):
        _valid = True
        for dir in dirs:
            if not os.path.isdir(dir):
                _valid = False
        return _valid


class HPCCFile(HPCCBase):

    def __init__(self, file):
        self.rawFile = file
        try:
            self.__fileParts()
            self.__version()
            self.__getOS()
            self.__getMD5()
            self.__getSize()
        except Exception as e:
            raise e

    def __version(self):
        self.version = self.get_ver_string(self.file)

    def __fileParts(self):
        if not os.path.isfile(self.rawFile):
            raise HPCCError(1000,
                    "File does not exist: {0}".format(self.rawFile)
                )
        self.file = os.path.basename(self.rawFile)
        self.path = os.path.dirname(self.rawFile)

    def __getOS(self):
        for os in OS:
            for id in OS[os]:
                meta_pattern = "*" + id['id'] + "*"
                install_pattern = "*" + id['install'] + "*"
                if (fnmatch.fnmatch(self.file, meta_pattern) and
                    fnmatch.fnmatch(self.file, install_pattern)):
                    self.os = os
                    self.install = id['install']
                    self.osTemplate = id


    def __getMD5(self):
        try:
            md5 = hashlib.md5()
            with open(self.rawFile) as f:
                for chunk in iter(lambda: f.read(8192), ''):
                    md5.update(chunk)
            self.md5 = md5.hexdigest()
        except:
            raise HPCCError(1002,
                "Cannot create md5: {0}".format(self.rawFile)
                )

    def __getSize(self):
        try:
            self.size = "%0.3f MB" % (
                    os.path.getsize(self.rawFile) / (1024 * 1024.0)
                )
        except:
            raise HPCCError(1003,
                "Cannot getsize: {0}".format(self.rawFile)
                )

    def getRelativePath(self, buildDir):
        if self.rawFile.startswith(buildDir):
            return self.rawFile[len(buildDir):]


class HPCCVersionSet(HPCCBase):

    def __init__(self, buildDir, version):
        self.buildDir = buildDir
        self.version = version
        self.files = list()
        try:
            self.getFiles()
            self.versionParts = self.get_ver_dict(self.version)
        except Exception as e:
            raise e

    def getFiles(self):
        files = self.get_file_list(self.buildDir, self.version)
        for file in files:
            self.addFile(file)

    def addFile(self, file):
        self.files.append(HPCCFile(file))


class HPCCBuildSet(HPCCBase):

    def __init__(self, buildSet):
        self.buildSet = buildSet
        self.name = os.path.basename(buildSet)
        try:
            self.getBuildSet()
        except Exception as e:
            raise e

    def getBuildSet(self):
        self.versions = self.get_ver_list(self.buildSet)

    def getVersionSets(self, version=False):
        versionSets = list()
        if not version:
            for ver in self.versions:
                versionSets.append(HPCCVersionSet(self.buildSet, ver))
        else:
            versionSets = HPCCVersionSet(self.buildSet, version)
        return versionSets


class HPCCBuilds(HPCCBase):

    builds = list()

    def __init__(self, buildDir):
        self.buildDir = buildDir
        self.builds = list()
        try:
            self.getBuilds()
        except Exception as e:
            raise e

    def getBuilds(self):
        if not os.path.isdir(self.buildDir):
            raise HPCCError(2000,
                "Build dir does not exist: {0}".format(self.buildDir)
                )
        for d in os.listdir(self.buildDir):
            path = os.path.join(self.buildDir, d)
            dirs = self.genBuildDirs(path)
            if os.path.isdir(path):
                if self.checkDirs(dirs):
                    self.builds.append(d)

    def getBuildSets(self, buildD=False):
        buildSets = list()
        if not buildD:
            for build in self.builds:
                path = os.path.join(self.buildDir, build)
                buildSets.append(HPCCBuildSet(path))
        else:
            path = os.path.join(self.buildDir, buildD)
            buildSets = HPCCBuildSet(path)
        return buildSets


if __name__ == "__main__":
    bH = HPCCBuilds(BUILD_DIR)
    bS = bH.getBuildSets("CE-Candidate-4.0.0")
    vS = bS.getVersionSets("4.0.0-1")
    print vS.version
