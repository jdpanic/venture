from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    url(r'^game$', 'venture.views.game'),
    url(r'^action/$', 'venture.views.action'),
    url(r'^quit/$', 'venture.views.quit'),
    url(r'^login/$', 'venture.views.login'),
    url(r'^$', 'venture.views.main'),
)
