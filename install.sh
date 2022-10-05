#! /bin/bash
project_name=$1
application_name=$2
pip install django
pip freeze > requirements.txt

#setup new project

django-admin startproject $project_name


#Applications des migrations
(cd $project_name;python manage.py migrate)

#creation de l'application

(cd $project_name;python manage.py startapp $application_name)
mkdir -p $project_name/$application_name/templates/$application_name
mkdir -p $project_name/$application_name/static/$application_name
(cd $project_name/$application_name; touch form.py)

#demarrage du serveur
(cd $project_name;python manage.py runserver) 




