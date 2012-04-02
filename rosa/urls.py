from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
#from application.views import home
from views import home, about

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',       home, name='home'),
    url(r'^about$',  about, name='about'),
    # url(r'^help$', direct_to_template, {'template': 'help.html'}, name='help'),

    url(r'^application/', include('application.urls')),
    # url(r'^report/', include('report.urls')),
    # url(r'^search/', include('search.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
