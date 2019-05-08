from django.conf.urls import url
from django.http import HttpResponse

DEBUG = True
SECRET_KEY = 'woshiyigedashabi'
ROOT_URLCONF = __name__

def home(request):
    return HttpResponse('Welcome to the Tinyapp\'s Homepage!')

urlpatterns = [
    url(r'^test/$', home),
]
