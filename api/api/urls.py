"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf.urls import url
from django.http import HttpResponse
from searcher import PackageSearcher
from searcher import DescriptionSearcher

DEBUG = True
SECRET_KEY = 'woshiyigedashabi'
ROOT_URLCONF = __name__

def home(request):
    print("----------------------")
    return HttpResponse('Welcome to the Tinyapp\'s Homepage!')

def test(request):
    queryContent = "express"
    print("query is: ",  queryContent)
    searcher = PackageSearcher("config.toml")
    results = searcher.search(queryContent)
    # return jsonify(results)
    print(results)
    return HttpResponse(results)


urlpatterns = [
    path('admin/', admin.site.urls),
    # url('', home, name='index'),
    path('test/', test),
]
