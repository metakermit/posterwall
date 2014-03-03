from django.conf.urls import url, patterns

urlpatterns = patterns(
    '',
    url('^$', 'posterwall.apps.events.views.events_view', name='events_view'),
)

