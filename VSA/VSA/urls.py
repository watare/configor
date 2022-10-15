"""VSA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ovs_conf import views

urlpatterns = [
    path("/admin/", admin.site.urls),
    path("base/",views.base,name='base'),
    path("generate_ovs/",views.generate_ovs,name='generate_ovs'),
    path("bridge_create/",views.bridge_create,name='bridge_create'),
    path("bridgeDetails/<int:id>",views.bridgeDetails,name='bridgeDetails'),
    path("bridge_list/",views.bridge_list,name='bridge_list'),
    path("generateOvsConfiguration/",views.generateOvsConfiguration,name='generateOvsConfiguration'),
    path("generateVmConfiguration/",views.generateVmConfiguration,name='generateVmConfig')
]
