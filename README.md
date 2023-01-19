# CONFIGOR


## Tree Structure

- configor/ - Project Directory
- configor/configor/ - Django Project Directory
- configor/configor/settings.py - Django Project Settings
- ovs_conf/ - Django App Directory

```
.
├── configor
│   ├── configor
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   ├── manage.py
│   ├── ovs_conf
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── form
│   │   │   ├── __init__.py
│   │   │   ├── ovsForm.py
│   │   │   ├── __pycache__
│   │   │   └── vmForm.py
│   │   ├── __init__.py
│   │   ├── media
│   │   │   └── ovs_conf
│   │   │       ├── simpletemplate.xml
│   │   │       ├── templateUPdated.xml
│   │   │       └── template.xml
│   │   ├── migrations  [24 entries exceeds filelimit, not opening dir]
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── ovsModels.py
│   │   │   ├── __pycache__
│   │   │   └── vmsModels.py
│   │   ├── __pycache__
│   │   ├── static
│   │   │   └── ovs_conf
│   │   │       ├── css
│   │   │       ├── js
│   │   │       └── style.css
│   │   ├── templates
│   │   │   └── ovs_conf
│   │   │       ├── base.html
│   │   │       ├── bridge_create.html
│   │   │       ├── bridgeDetails.html
│   │   │       ├── bridge_list.html
│   │   │       ├── generateOvsConfiguration.html
│   │   │       ├── generateVmConfiguration.html
│   │   │       └── ports_create.html
│   │   ├── test
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   └── testModels.py
│   │   └── views
│   │       ├── foo.py
│   │       ├── __init__.py
│   │       ├── ovsViews.py
│   │       ├── __pycache__
│   │       └── vmsViews.py
│   └── ovs.yaml
├── install.sh
├── License.md
├── README.md
└── requirements.txt
```
