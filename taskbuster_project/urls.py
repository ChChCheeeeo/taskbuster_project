# -*- coding: utf-8 -*-
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from django.contrib import admin

from .views import home, home_files

urlpatterns = [
    # Examples:
    #url(r'^$', 'taskbuster_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # take desired urls and passes as an argument the 
    # filename (i.e. robots.txt or humans.txt)
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        home_files, name='home-files'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'i18n/', include('django.conf.urls.i18n')),
]

# left the robots.txt and humans.txt files with the same url
# include langauge translation(e.g /en/) to url
urlpatterns += i18n_patterns(
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
)