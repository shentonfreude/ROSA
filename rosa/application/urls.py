from django.conf.urls.defaults import * #GROSS
#from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import list_detail
#from django.views.generic.create_update import create_object

from models import Application
#from views import csvimport, list_apps, list_app_versions, version_details
from views import application_versions, app_details


#from views import search, browse, approved, closed
applications = {
    'queryset' : Application.objects.all().order_by('acronym', 'release')
    }
# Cannot do .order_by('acronym').distinct('acronym') DISTINCT ON field in SQLite

urlpatterns = patterns(
    '',
    url(r'^$',                  list_detail.object_list, applications, name='list_apps'),
    url(r'^all$',               application_versions, name='app_versions'),
    url(r'^(?P<object_id>\d+)$',       app_details, name='app_details'),
    # url(r'^(?P<object_id>\d+)$',  list_app_versions, name="list_app_versions"),
    # url(r'^version/(?P<object_id>\d+)$',  version_details, name="version_details"),
    # url(r'^csvimport$',        csvimport, name="csvimport"),
#    url(r'^$',                     browse, name="projects"),
#    url(r'^approved$',             approved, name="approved"),
#    url(r'^closed$',               closed, name="closed"),
#    url(r'^search/$',              search, name="search"),
#    url(r'^new/$',                 create_object, {'model': Application}), # For admins only
)

