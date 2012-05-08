from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("", 
    url(r'^game/$', 'venture.views.game'),
    url(r'^action/$', 'venture.views.action'),
    url(r'^quit/$', 'venture.views.quit'),
    url(r'^logout/$', 'venture.views.logout'),
    url(r'^person/new/$', 'venture.views.new_person'),
    url(r'^person/([0-9]+)/$', 'venture.views.choose'),
    url(r'^login/$', 'venture.views.login'),
    url(r'^person/$', 'venture.views.choose'),
    url(r'^reset/$', 'venture.views.reset'),
    # url(r'^quests/$', 'venture.views.quests'),
    url(r'^$', 'venture.views.login'),
)
