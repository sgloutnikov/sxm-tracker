from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.nowplaying, {'page': str(1)}, name='index'),
    url(r'^nowplaying/(?P<page>([1-9][0-9]{0,1}))/$', views.nowplaying, name='nowplayingpage')
]
