"""CatanApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^newGame/', newGame),
    url(r'^build/',build),
    url(r'^endOfTurn/', endOfTurn),
    url(r'^placeRobber/',placeRobber),
    url(r'^buildRoad/', buildRoad),
    url(r'^buildSettlement/', buildSettlement),
    url(r'^buildCity/', buildCity),
    url(r'^buyCard/', buyCard),
    url(r'^playCard/', playCard),
    url(r'^portTrade/', portTrade),
    url(r'^bankTrade/',bankTrade),
    url(r'^playerTrade/',playerTrade),
    url(r'^tradeMaker/', tradeMaker)
]
