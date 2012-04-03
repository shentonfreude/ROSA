from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template, redirect_to
#from application.views import home
from views import home, about

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',                  home,           name='home'),
    url(r'^about$',             about,          name='about'),

    url(r'^application/',       include('application.urls')),
    url(r'^report/',            include('report.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # This is a hack to make the menu bar cog link work.
    # django/contrib/admin/sites.get_urls says ^$ is 'index' -- how to use?
    url(r'^admin$',             redirect_to, {'url': '/admin/'}, name='manage'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/',             include(admin.site.urls)),
)
