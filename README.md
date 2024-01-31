ON Generation For HPCC Systems Releases
This implementation is based on old Python 2.7 and old Django.
This repo should be upgraded to Python 3.x and new Django or other frame work.

## Installation
### Python 2.7
Python2.7. For CentOS default python is 2.6.6 which is not good enough. Following these steps to install Python2.7:
1. yum groupinstall "Development tools"
2. yum install zlib-devel
   yum install bzip2-devel
   yum install openssl-devel
   yum install ncurses-devel
3. wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
   tar xf Python-2.7.3.tar.bz2
   cd Python-2.7.3
   ./configure --prefix=/usr/local
   make && make altinstall
4. cd /usr/local/bin
   ln -s /usr/local/bin/python2.7 /usr/local/bin/python


### Django
Reference https://docs.djangoproject.com/en/1.5/topics/install/#installing-official-release for other options
1. Install python setuptools:
   wget https://bootstrap.pypa.io/ez_setup.py
   python ez_setup.py
2. Install python-pip:
   https://bootstrap.pypa.io/pip/2.7/get-pip.py
   python get-pip.py
3. pip install Django (for Python 2.7.11 pip install Django=1.4.22 work with our staging script)

To use Django with nginx install and configure nginx:
- For Ubuntu directly run sudo apt-get install nginx
- For CentOS before run yum install nginx create a /etc/yum.repos.d/nginx.repo:
```code
[nginx]
  name=nginx repo
  baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
  gpgcheck=0
  enabled=1
```
- replace or create /etc/nginx/sites-available/defauilt with this file. Also replace /etc/nginx/nginx with nginx.conf
- To start nginx: service nginx start

Some update:
- Django 1.9 does not ship simplejson. It need install as pip install simplejson
- Django 1.9 drop FastCGI support. The app can not be started with current start script. Need some investigation
- I switch back to Django 1.5.4 (pip install Django==1.5.4). And uninstall external simplejson: pip uninstall simplejson it works!

django.conf.urls.defaults removed
From Djando version 1.6.0 django.conf.urls.defaults is removed. Directory use django.conf.urls instead.

replace simplejson
Simplejons module will cause namedtuple_as_object exception.
- In our staging code we will replace it with json model (also replacing simplejson.dump wtih json.dump).
- The similar thing need done for piston/emitters.py version 0.2.3 (probably under /usr/local/lib/<python>
```code
#from django.utils import simplejson
 import json
 ...
 #seria = simplejson.dumps(self.construct(), cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
 seria = json.dumps(self.construct(), cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
 ...
 #Mimer.register(simplejson.loads, ('application/json',))
 Mimer.register(json.loads, ('application/json',))
```

### piston
1. Download django-piston from https://pypi.python.org/pypi/django-piston/. The current latest is 0.2.3. Untar the file.
2. Go to untar the directory and run python setup.py install

### flup
1. https://pypi.python.org/pypi/flup/1.0.2 (can't use 1.0.3 which will has missing module _dummy_thread error
2. untar and cd to the directory run python setup.py install

## Web Server
Assume using nginx
### Mount build directory
```code
git clone this repo <HPCC_Build_Staging>
mount <file server>:/<base>/hpcc/builds   <HPCC_Build_Staging>/tBuilds>
```
If mount to other place make sure update 
```code
BuildStaging/settings.py:BUILD_DIR = os.path.join(BASE_DIR,"../tBuilds")
```

### Sample configuration file
./nginx/sites-available/default

### Start/Stop
- Stop: ./stop
- Start: ./start (start script will stop the app and restart it)

### log file
Console outputs are defined in start script. Currently there are /tmp/out.log and /tmp/err.log
To add logging using "print" which will go to /tmp/out.log

## Update 
Edit /u/BuildStaings/Buildstaging/stagingconfig.py
pre 4.0.0 builds are commented out in this file.


## Troubleshooting
### Unrecognized version displayed as "Unknown"
Previous unrecognized version will cause exception throwing which will terminate the json process. For example, Kel file KEL-0.5.4.zip. To workaround this we just print out the version as "Unknown" and continue process other files and versions. Source file: api/module.py/get_ver_string(self, file)


## Build Files
### A Sample Tree List
tree-CE-9.4.20-bin
This file list CE-Candidate-9.4.20/bin which contains two builds: 1) A candidate build: 9.4.20-rc1 2) A gold build: 9.4.20-1
