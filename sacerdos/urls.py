from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                           'document_root': settings.MEDIA_ROOT,
                       }),
                       url(r'^', include('wallfly.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
