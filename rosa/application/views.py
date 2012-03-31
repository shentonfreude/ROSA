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


class SearchForm(Form):
    text   = CharField(max_length=80, required=True)

def search(request):
    """Search common fields for substring match:
    acronym, name, description, ...
    TODO: We should match what ROSA does, even if it's dumb.
    """
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            q = Q(acronym__icontains=text)
            q = q | Q(app_name__icontains=text)
            q = q | Q(description__icontains=text)
            apps = Application.objects.filter(q).order_by('acronym', 'release')
            return render_to_response('application/search_results.html',
                                      {'object_list': apps},
                                      context_instance=RequestContext(request));
    else:
        form = SearchForm()
    return render_to_response('application/search.html',
                              {'form': form},
                              context_instance=RequestContext(request));


def report(request):
    """Show page offering different reports. Boring.
    """
    return render_to_response('application/report.html',
                              context_instance=RequestContext(request));

def report_current(request):
    """Show page offering different reports. Boring.
    """
    apps = Application.objects.filter(app_status__name__icontains='Current').order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps},
                              context_instance=RequestContext(request));

def report_development(request):
    """Show page offering different reports. Boring.
    """
    apps = Application.objects.filter(app_status__name__icontains='Development').order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps},
                              context_instance=RequestContext(request));
