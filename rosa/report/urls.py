from django.conf.urls.defaults import * #GROSS
from django.views.generic import list_detail

from application.models import Application
#from views import acronyms, application_versions, app_details, search
from views import report, current, development
from views import app_pipeline_abbrev, app_pipeline_full


urlpatterns = patterns(
    '',
    url(r'^$',                          report,                 name='report'), # need slash?

    url(r'^current/$',                  current,                name='report_current'),
    url(r'^development/$',              development,            name='report_development'),

    url(r'^app_pipeline_abbrev$',       app_pipeline_abbrev,    name='report_app_pipeline_abbrev'),
    url(r'^app_pipeline_full$',         app_pipeline_full,      name='report_app_pipeline_full'),
)

