from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    #url(r'^$', 'posterwall.views.home', name='home'),
    url(r'^$', 'posterwall.views.grunt_test', name='grunt_test'),
    url(r'^admin/', include(admin.site.urls)),
)
