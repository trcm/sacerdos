from django.conf.urls import patterns, url
from wallfly import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = patterns('',
                       # url(r'^login/$', views.LoginView.as_view()),
                       # these two get the authentication system working
                       # grab the token for a use
                       url(r'^api-token-auth', obtain_auth_token),
                       # get the user details
                       url(r'^auth/$', views.AuthView.as_view(), name='auth'),
                       # grab all the details for a particular property
                       url(r'property/(?P<pk>[0-9]+)$', views.PropertyDetail.as_view(), name='properties'),
                       # get all the properties
                       url(r'property/$', views.PropertyView.as_view(), name='property'),
                       # get all the data and proeprties for an agent
                       url(r'agent/(?P<pk>[0-9]+)$', views.AgentView.as_view(), name='agent'),
                       url(r'user/(?P<pk>[0-9]+)$', views.UserDetail.as_view(), name='user'),

                       # grab or create an issue
                       url(r'issue/(?P<pk>[0-9]+)$', views.IssueDetail.as_view(), name='issue'),
                       # get all issues for a property 
                       url(r'issues/(?P<pk>[0-9]+)$', views.IssueList.as_view(), name='issue'),

                       # these two are special routes, the bottom one is what we should user
                       # but the second from the bottom lets us get to the django backend admin
                       url(r'^$', views.home, name='index'),
                       # url(r'.*$', views.home, name='index')
)

