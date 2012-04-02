import logging

from collections import OrderedDict

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import Form, CharField, DateField, ModelMultipleChoiceField
from django.forms import SelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Application

logging.basicConfig(level=logging.INFO)


class SearchForm(Form):
    text   = CharField(max_length=80, required=True)

BOOTSTRAP_LABEL = {
    "Archived"          : "label",               # gray
    "Cancelled"         : "label label-inverse",   # black
    "Current Version"   : "label label-success",   # green
    "In Development"    : "label label-info",      # blue
    "In Suspense"       : "label label-important", # red
    "Inactive"          : "",
    "Moved"             : "",
    "Prior Version"     : "",
    "Roll Back"         : "",
    "Unassigned"        : "label label-warning",   # yellow
}

def acronym_status_class(acronym):
    """Return Bootstrap color coded class name based on acronym.
    The different releases of an acronym will have different app_status,
    and we prefer to show Development to Current.
    """
    statuses = Application.objects.filter(acronym=acronym).values_list('app_status__name', flat=True).distinct()
    if "In Development" in statuses: # prefer to show Development to Current
        return BOOTSTRAP_LABEL["In Development"]
    elif "Current Version" in statuses:
        return BOOTSTRAP_LABEL["Current Version"]
    else:
        return ""

# Try improving speed with Applicaiton.objects.prefetch_related()

#select distinct acronym, application_appstatus.name from application_application, application_appstatus;
# select distinct application_appstatus.name from application_application, application_appstatus where acronym="PAVE";

def acronyms(request, acronym=None):
    if not acronym:
        # Can we pull the list of app_status in the same query??
        acros = Application.objects.values_list('acronym', flat=True).distinct().order_by('acronym')
        alphabin = OrderedDict()
        #acronym_class = {}
        for acro in acros:   # without 'flat' values_list list of tuples [(u'AAIS',), (u'ACDS',)]
            # alphabin them by acronym
            c = acro[0]
            if c not in alphabin:
                alphabin[c] = []
            acro_class = acronym_status_class(acro)
            alphabin[c].append((acro, acro_class))

        ret_dict = {'alphabin': alphabin,
                    }
        return render_to_response('application/acronyms.html',
                                  ret_dict,
                                  context_instance=RequestContext(request));
    apps = Application.objects.filter(acronym__iexact=acronym).order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps},
                              context_instance=RequestContext(request));

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
