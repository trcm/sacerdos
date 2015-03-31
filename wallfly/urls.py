from django.conf.urls import patterns, url
from wallfly import views

urlpatterns = patterns('',
                       url(r'property/$', views.PropertyView.as_view(), name='properties'),
                       url(r'.*$', views.home, name='index')
                       )
