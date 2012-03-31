from django.conf.urls.defaults import * #GROSS
#from django.views.generic.list_detail import object_list, object_detail
from django.views.generic import list_detail
#from django.views.generic.create_update import create_object

from models import Application
#from views import csvimport, list_apps, list_app_versions, version_details
from views import list_apps


#from views import search, browse, approved, closed
applications = {
    'queryset' : Application.objects.all().order_by('acronym', 'release')
    }

urlpatterns = patterns(
    '',
    url(r'^$',                  list_detail.object_list, applications, name='list_apps'),
    # url(r'^(?P<object_id>\d+)$',  list_app_versions, name="list_app_versions"),
    # url(r'^version/(?P<object_id>\d+)$',  version_details, name="version_details"),
    # url(r'^csvimport$',        csvimport, name="csvimport"),
#    url(r'^$',                     browse, name="projects"),
#    url(r'^approved$',             approved, name="approved"),
#    url(r'^closed$',               closed, name="closed"),
#    url(r'^search/$',              search, name="search"),
#    url(r'^new/$',                 create_object, {'model': Application}), # For admins only
)

