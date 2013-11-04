OS = [
    {
    "os": "centos",
    "id": "el5",
    "name": "CentOS",
    "install": "platform",
    "title": "HPCC Platform Centos5",
    "text": "",
    "link": ""
    },
    {
    "os": "centos",
    "id": "el6",
    "name": "CentOS",
    "install": "platform",
    "title": "HPCC Platform Centos6",
    "text": "",
    "link": ""
    },
    {
    "os": "debian",
    "id": "squeeze",
    "name": "Debian",
    "install": "platform",
    "title": "HPCC Platform Debian Squeeze",
    "text": "",
    "link": ""
    },
    {
    "os": "mac",
    "id": "Darwin",
    "name": "MacOSX",
    "install": "clienttools",
    "title": "Client Tools for Mac OSX",
    "text": "",
    "link": ""
    },
    {
    "os": "opensuse",
    "id": "suse11.4",
    "name": "OpenSUSE",
    "install": "platform",
    "title": "HPCC Platform OpenSUSE 11.4",
    "text": "",
    "link": ""
    },
    {
    "os": "ubuntu",
    "id": "lucid",
    "name": "Ubuntu",
    "install": "platform",
    "title": "HPCC Platform Ubuntu 10.04 LTS",
    "text": "",
    "link": ""
    },
    {
    "os": "ubuntu",
    "id": "natty",
    "name": "Ubuntu",
    "install": "platform",
    "title": "HPCC Platform Ubuntu 11.04",
    "text": "",
    "link": ""
    },
    {
    "os": "ubuntu",
    "id": "oneiric",
    "name": "Ubuntu",
    "install": "platform",
    "title": "HPCC Platform Ubuntu 11.10",
    "text": "",
    "link": ""
    },
    {
    "os": "ubuntu",
    "id": "precise",
    "name": "Ubuntu",
    "install": "platform",
    "title": "HPCC Platform Ubuntu 12.04 LTS",
    "text": "",
    "link": ""
    },
    {
    "os": "windows",
    "id": "ECLIDE",
    "name": "Windows",
    "install": "clienttools",
    "title": "ECL IDE and Client Tools for Windows",
    "text": "",
    "link": ""
    },
    {
    "os": "windows",
    "id": "GraphControl.",
    "name": "Windows",
    "install": "clienttools",
    "title": "Graph Control for Windows 32 bit",
    "text": "",
    "link": ""
    },
    {
    "os": "windows",
    "id": "GraphControl64",
    "name": "Windows",
    "install": "clienttools",
    "title": "Graph Control for Windows 64 bit",
    "text": "",
    "link": ""
    },
    {
    "os": "windows",
    "id": "Windows",
    "name": "Windows",
    "install": "clienttools",
    "title": "Client Tools for Windows",
    "text": "",
    "link": ""
    },
    {
    "os": "all",
    "id": "VM",
    "name": "all",
    "install": "platform",
    "title": "HPCC VM Image",
    "text": "Release Notes",
    "link": "/downloads/vm-release-notes#"
    }
]

id = 1
for temp in OS:
    print '- model: api.OsTemplate'
    print '  pk: '+`id`
    print '  fields:'
    for k,v in temp.items():
        if v:
            print '    T'+k+': '+v
    id = id + 1
