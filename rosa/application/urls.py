from django.conf.urls.defaults import * #GROSS
from django.views.generic.list_detail import object_detail
from django.views.generic.create_update import create_object
from models import Application
from views import csvimport

#from views import search, browse, approved, closed
info_dict = {
    'queryset' : Application.objects.all()
    }

urlpatterns = patterns(
    '',
    url(r'^csvimport$',        csvimport, name="csvimport"),
#    url(r'^$',                     browse, name="projects"),
#    url(r'^approved$',             approved, name="approved"),
#    url(r'^closed$',               closed, name="closed"),
#    url(r'^search/$',              search, name="search"),
#    url(r'^(?P<object_id>\d+)/$',  object_detail, info_dict, name="details"),
#    url(r'^new/$',                 create_object, {'model': Application}), # For admins only
)

