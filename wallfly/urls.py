from django.conf.urls import patterns, url
from wallfly import views

urlpatterns = patterns('',
                       url(r'property/$', views.PropertyView.as_view(), name='properties'),
                       url(r'agent/(?P<pk>[0-9]+)$', views.AgentView.as_view(), name='agent'),
                       url(r'user/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user'),
                       url(r'^$', views.home, name='index'),
                       url(r'.*$', views.home, name='index')
)

