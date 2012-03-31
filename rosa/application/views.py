# Create your views here.
# Fuck, do I really have to make a view for this? 

from collections import OrderedDict

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import Form, CharField, DateField, ModelMultipleChoiceField
from django.forms import SelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import logging
logging.basicConfig(level=logging.INFO)

#from models import Project, Center, Status


from csv import DictReader
from models import Application
#, Version, OrganizationalAcronym, TaskOrder, ApplicationType, SoftwareClass, ReleaseStatus
#from models import InformationSensitivity, AuthenticationMethod, TriageLevel, ApplicationUserGroup, FrequencyUsed

def list_apps(request):
    return render_to_response('list_apps.html',
                              {'apps': Application.objects.all().order_by('acronym', 'release'),
                               },
                              context_instance=RequestContext(request));

def application_versions(request):
    """Return sorted list of Arco and Versions
    ['Acro': [<appv1>, <appv2>, ...], 'Zeta':[<apps>...]]
    Render like:
    BESS  1.1, 1.2, 2.1
    CATS  2.0, 2.3, 2.4
    """
    apps = Application.objects.all().order_by('acronym', 'release')
    appvers = OrderedDict()
    for app in apps:
        acro = app.acronym
        if not acro in appvers:
            appvers[acro] = []
        appvers[acro].append(app)
    return render_to_response('application/application_versions.html',
                              {'application_versions': appvers
                               },
                              context_instance=RequestContext(request));

def app_details(request, object_id):
    """Return full application.
    Shouldn't this be done with Generic View? 
    """
    return render_to_response('application/application_details.html',
                              {'app': Application.objects.get(pk=object_id)
                               },
                              context_instance=RequestContext(request));



# def list_app_versions(request, object_id):
#     # Bug: we have multiple versions of each App on import
#     # so we can't use our pk, we have to use the acronym for now
#     #objs = Version.objects.filter(application=object_id) # FK
#     app = Application.objects.get(pk=object_id)
#     objs = Version.objects.filter(application__acronym=app.acronym) # FK
#     return render_to_response('list_app_versions.html',
#                               {'objs': objs,
#                                },
#                               context_instance=RequestContext(request));

# def version_details(request, object_id):
#     version= Version.objects.get(pk=object_id)
#     return render_to_response('version_details.html',
#                               {'version': version,
#                                },
#                               context_instance=RequestContext(request));


def get_fk(model, name):
    """Find name in model, if not there, create it. Return key.
    use: get_fk(OrganizationalAcronym, row['nasa_owner_office_id'])
    CAVEAT: this will pollute our DB with useless "Unspecified" and "UNSPECIFIED"
    types of entries. Maybe we can defend against these specific words?
    """
    try:
        item = model.objects.get(name=name)
    except model.DoesNotExist:
        item = model(name=name)
        item.save()
        logging.info("get_fk model=%s name=%s : CREATED item=%s" % (model, name, item))
    return item

def isodate(slashdate):
    """convert CSV's 01/12/2012 to django 2012-01-12.
    Doesn't honor "input_formats" from DateField (Field, not Model?)
    '01/12/2012' => [u'Enter a valid date in YYYY-MM-DD format.']
    Why isn't it converting with DATE_INPUT_FORMATS
    or the default long set of formats? Maybe only on forms?
    """
    # try converting to time and then strftime or iso:
    # time.strptime(stamp, '%b %d %Y %I:%M%p'). 
    (m, d, y) = slashdate.split("/")
    return "%s-%s-%s" % (y, m, d)

# 'release_date',
# 'version_number',
# 'b1',
# 'Application.acronym',
# 'service_request_numbers',
# 'nasa_owner_office_id',
# 'b2',
# 'nasa_owner_name',
# 'version_change_description',
# 'b3',
# 'contract_task_order_numbers',
# 'b4',
# 'application_type',
# 'software_class',
# 'Application.name',
# 'architecture_type',
# 'b5',
# 'version_status']


### BUG: we're creating multiple versions of an App

# def csvimport(request):
#     csvfile = open("rosa-app-pipeline-full.csv")
#     reader = DictReader(csvfile)
#     logging.info("fieldnames=%s" % reader.fieldnames)

#     for row in reader:
#         if not row['release_date']:
#             continue
#         logging.info("%(release_date)s %(application.acronym)s %(version_number)s %(nasa_owner_office_id)s %(nasa_requester)s %(contract_task_order_numbers)s %(application_type)s %(architecture_type)s %(version_status)s" % row)

#         app = Application.objects.filter(name=row['application.acronym'])
#         if not app:
#             app = Application(acronym=row['application.acronym'], name=row['application.name'])
#             app.save()

#         nasa_owner_office_id              = get_fk(OrganizationalAcronym, row['nasa_owner_office_id'])
#         contract_task_order_numbers       = get_fk(TaskOrder,             row['contract_task_order_numbers'])
#         application_type                  = get_fk(ApplicationType,       row['application_type'])
#         software_class                    = get_fk(SoftwareClass,         row['software_class'])
#         version_status                    = get_fk(ReleaseStatus,         row['version_status'])

#         # check out Modelname.objects.create() call instead?

#         version = Version(application=app,
#                           release_date=isodate(row['release_date']),
#                           version_number=row['version_number'],
#                           service_request_numbers=row['service_request_numbers'],
#                           nasa_owner_office_id=nasa_owner_office_id,
#                           nasa_requester=row['nasa_requester'],
#                           version_change_description=row['version_change_description'],
#                           application_type=application_type,
#                           software_class=software_class,
#                           version_status=version_status,
#                           # These may not be Null, why not?
#                           information_sensitivity = get_fk(InformationSensitivity, 'Not In Rosa Report'),
#                           authentication_type     = get_fk(AuthenticationMethod,   'Not in Rosa Report'),
#                           odin_triage_level       = get_fk(TriageLevel,            'Not in Rosa Report'),
#                           user_groups             = get_fk(ApplicationUserGroup,   'Not in Rosa Report'),
#                           frequency_used          = get_fk(FrequencyUsed,          'Not in Rosa Report'),
#                           architecture_type       = get_fk(ApplicationType,        'Not in Rosa Report'), 
#                           )
#         # Also not in Rosa Report:
#         # * primary deveoper
#         # Invalid keyword argument:
#   #contract_task_order_numbers=contract_task_order_numbers,

#         version.save()
#     return HttpResponseRedirect(reverse('home'))



