# Project Requirements

## Input Files
### OS and Packages List
Prefer a YAML file
Reference file BuildStaging/stagingconfig.py

Ubuntu: 
  24.04, 22.04 and 20.04
Rocky Linux:
  8
CentOS 
  7, Stream 8
Windows
  x64 (Clienttools), i386 (ECLIDE)

OSX (Clientools)

### Packages File Pattern
Any file format, either plain text or yaml, etc
It is OK if combined with "OS and Packages List" file
Reference file BuildStaging/stagingconfig.py
VERSION_RE = r'(?:(\d{1,2})\.)(?:(\d{1,2})\.)(\d{1,})(\-|\.|\~)(\d{1,2}|rc|closedown|beta|alpha|trunk)(\d{1,2})?'
VERSION_RE_NORMALIZED = r'(?:(\d{1,2})\.)(?:(\d{1,2})\.)(\d{1,})(\-|\~)(\d{1,2}|rc|closedown|beta|alpha|trunk)(\d{1,2})?'

Probably only one of above is really used

### Docker Image
Put all code and dependcies in a Docker image with a READMD.md
When user run app it should only need a Docker environment and nothing else

## Script Language
The first choice can be any language such as bash, python.
It is optional, if have time, to upgrade current Django framework (Last Django version + Python3 + Nginx)

## Additional thinking
It is optional. Try to use Github Copilot and write a report about the experience and tricks & tips, etc

## GitHub Repo
Create a GitHub repo to host the project and instruction to run and maintain the project
