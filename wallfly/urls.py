from django.conf.urls import patterns, url
from wallfly import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
                       # url(r'^login/$', views.LoginView.as_view()),
                       url(r'^api-token-auth', obtain_auth_token),
                       url(r'^auth/$', views.AuthView.as_view(), name='auth'),
                       url(r'property/(?P<pk>[0-9]+)$', views.PropertyDetail.as_view(), name='properties'),
                       url(r'property/$', views.PropertyView.as_view(), name='property'),
                       url(r'agent/(?P<pk>[0-9]+)$', views.AgentView.as_view(), name='agent'),
                       url(r'user/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user'),
                       url(r'issue/(?P<pk>[0-9]+)$', views.IssueDetail.as_view(), name='issue'),
                       url(r'issues/(?P<pk>[0-9]+)$', views.IssueList.as_view(), name='issue'),
                       url(r'^$', views.home, name='index'),
                       # url(r'.*$', views.home, name='index')
)

