import logging
import time
import json
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

BOOTSTRAP_LABEL = {                                # underscore names for template access
    "Archived"          : "label",                 # gray
    "Cancelled"         : "label label-inverse",   # black
    "Current Version"   : "label label-success",   # green
    "Current_Version"   : "label label-success",   # green
    "In Development"    : "label label-info",      # blue
    "In_Development"    : "label label-info",      # blue
    "In Suspense"       : "label label-important", # red
    "In_Suspense"       : "label label-important", # red
    "Inactive"          : "",
    "Moved"             : "",
    "Prior Version"     : "",
    "Prior_Version"     : "",
    "Roll Back"         : "",
    "Roll_Back"         : "",
    "Unassigned"        : "label label-warning",   # yellow
}

# TODO: memoize this
def _search_suggestions():
    """Provide suggestions to the search box.
    TODO: provide this on *every* view since the box is there.
    How to pull this request from Django template?
    """
    acros = Application.objects.values_list('acronym', flat=True).order_by('acronym').distinct()
    acros = [acro for acro in acros]
    acros = json.dumps(acros)
    import pdb; pdb.set_trace()
    return acros


def acronyms(request, acronym=None):
    # Query Application.objects.prefetch_related('app_status').\
    #    values_list('acronym', flat=True).distinct().order_by('acronym') 
    # took 5.2 seconds.
    # Query attrs we want and reducing with dicts takes 0.03 seconds, 173x speedup. :-)
    if not acronym:
        apps = Application.objects.values('acronym', 'app_status__name').order_by('acronym').distinct()
        acros = OrderedDict()
        for app in apps:
            acro = app.pop('acronym')
            if acro not in acros:
                acros[acro] = []
            acros[acro].append(app.pop('app_status__name'))
        alphabin = OrderedDict()
        for acro, statuses in acros.items():
            c = acro[0].upper()
            if c not in alphabin:
                alphabin[c] = []
            if "In Development" in statuses: # prefer to show Development to Current
                acro_class = BOOTSTRAP_LABEL["In Development"]
            elif "Current Version" in statuses:
                acro_class = BOOTSTRAP_LABEL["Current Version"]
            else:
                acro_class = ""
            alphabin[c].append((acro, acro_class))
        return render_to_response('application/acronyms.html',
                                  {'alphabin': alphabin,
                                   'bootstrap_label': BOOTSTRAP_LABEL,
                                   },
                                  context_instance=RequestContext(request));
    apps = Application.objects.filter(acronym__iexact=acronym).order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps,
                               'bootstrap_label': BOOTSTRAP_LABEL,
                               },
                              context_instance=RequestContext(request));

# def list_apps(request):
#     return render_to_response('list_apps.html',
#                               {'apps': Application.objects.all().order_by('acronym', 'release'),
#                                },
#                               context_instance=RequestContext(request));

def application_versions(request):
    """Return sorted list of Arco and Versions
    ['Acro': [<appv1>, <appv2>, ...], 'Zeta':[<apps>...]]
    Render like:
    BESS  1.1, 1.2, 2.1
    CATS  2.0, 2.3, 2.4
    alphabin={'A' : [{'AIIS': {'id': 1, 'release': '3.14', app_status__name='Prior'},
                              {'id': 2, 'release': '3.15', app_status__name='Current'},
                      'ARDVARK' : ...,
                     }],
              'B' : ...}
    Doing query for acros, then queries for release status,
    without prefetch: 2.7 seconds, with: 1.8
    Doing a single limited query of just the attrs we need: 0.05 seconds.
    """
    # Why is this getting a single app_status since it's M2M currently?
    apps = Application.objects.values('id', 'acronym', 'release', 'app_status__name').order_by('acronym', 'release')
    acro_vers = OrderedDict()
    for app in apps:
        acro = app.pop('acronym')
        if not acro in acro_vers:
            acro_vers[acro] = []
        app['app_class'] = BOOTSTRAP_LABEL.get(app.pop('app_status__name'), '')
        acro_vers[acro].append(app)
    alphabin = OrderedDict()
    for acro, releases in acro_vers.items():
        c = acro[0].upper()
        if c not in alphabin:
            alphabin[c] = []
        alphabin[c].append((acro, releases))
    return render_to_response('application/application_versions.html',
                              {'bootstrap_label': BOOTSTRAP_LABEL,
                               'alphabin': alphabin,
                               },
                              context_instance=RequestContext(request));

def app_details(request, object_id):
    """Return full application.
    Also show all other release versions for context.
    """
    app = Application.objects.get(pk=object_id)
    app_class = BOOTSTRAP_LABEL.get(app.app_status.all()[0].name, '') # all()[0] for bogus M2M
    rels = Application.objects.filter(acronym=app.acronym).values('id', 'release', 'app_status__name').order_by('release').distinct() # worthless 'distinct'
    releases = []
    # Is there a away to do this to 'rels' in place, or with a comprehension?
    for rel in rels:
        rel.update({'app_class': BOOTSTRAP_LABEL.get(rel.pop('app_status__name'))})
        releases.append(rel)
    return render_to_response('application/application_details.html',
                              {'app': app,
                               'app_class': app_class,
                               'releases': releases,
                               'bootstrap_label': BOOTSTRAP_LABEL,
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
            q = q | Q(owner__icontains=text)
            q = q | Q(owner_org__icontains=text)
            q = q | Q(nasa_off_name__icontains=text)
            q = q | Q(nasa_requester__icontains=text)
            q = q | Q(manager_app_development__icontains=text)
            q = q | Q(manager_project__icontains=text)
            q = q | Q(dev_name_primary__icontains=text)
            q = q | Q(dev_name_alternate__icontains=text)
            apps = Application.objects.filter(q).order_by('acronym', 'release')
            return render_to_response('application/search_results.html',
                                      {'object_list': apps,
                                       'bootstrap_label': BOOTSTRAP_LABEL,
                                       },
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
