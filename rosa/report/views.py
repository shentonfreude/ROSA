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

from application.models import Application
from application.views  import _search_suggestions, BOOTSTRAP_LABEL

logging.basicConfig(level=logging.INFO)



def report(request):
    """Show page offering different reports. Boring.
    """
    return render_to_response('report/report.html',
                              {'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));

def current(request):
    """Show page offering different reports. Boring.
    """
    apps = Application.objects.filter(app_status__name__icontains='Current').order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps,
                               'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));

def development(request):
    """Show page offering different reports. Boring.
    """
    apps = Application.objects.filter(app_status__name__icontains='Development').order_by('acronym', 'release')
    return render_to_response('application/search_results.html',
                              {'object_list': apps,
                               'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));

def app_pipeline_abbrev(request):
    """Actual, Projected, In-Suspense and TBD [wtf?]"
    rel date, release, acro, sr#, org acro, nasa requester, change description
    TODO: don't understand the status selection meanings above. Our choices:
      Cancelled, Archived, Prior Version, Current Version, Moved, Inactive,
      Roll Back, In Suspense, Unassigned, In Development.
    TODO: live server takes a from/two date
    """
    q =     Q(app_status__name__iexact='Current Version') # actual?
    q = q | Q(app_status__name__iexact='In Development')  # projected?
    q = q | Q(app_status__name__iexact='In Suspense')     # supense
    q = q | Q(app_status__name__iexact='Unassigned')      # TBD?
    apps = Application.objects.filter(q).values(
        'id', 'release_date', 'release', 'acronym', 'sr_number', 'owner_org',
        'nasa_requester', 'release_change_description', 'app_status__name',
        ).order_by('release_date', 'acronym', 'release')
    # TODO maybe inject app_class into results since
    # we can't deref by app.app_status__name there?
    return render_to_response('report/app_pipeline_abbrev.html',
                              {'object_list': apps,
                               'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));

def app_pipeline_full(request):
    """Actual, Projected, In-Suspense and TBD [wtf?]"
    rel date, release, acro, sr#, org acro, nasa requester, change description
    TODO: don't understand the status selection meanings above. Our choices:
      Cancelled, Archived, Prior Version, Current Version, Moved, Inactive,
      Roll Back, In Suspense, Unassigned, In Development.
    TODO: live server takes a from/two date
    TODO: use this query for _full and _abbrev report,
    just render with different templates
    """
    q =     Q(app_status__name__iexact='Current Version') # actual?
    q = q | Q(app_status__name__iexact='In Development')  # projected?
    q = q | Q(app_status__name__iexact='In Suspense')     # supense
    q = q | Q(app_status__name__iexact='Unassigned')      # TBD?
    apps = Application.objects.filter(q).values(
        # correct attrs above
        'id',
        'release_date',
        'release',
        'acronym',
        'sr_number',
        'owner_org',
        'nasa_requester',
        'release_change_description',
        # above in abbrev report too
        'sr_task_order',
        'functional_type__name', # Finance, Acct
        'software_category__name', # F
        'app_name',
        'architecture_type__name',    # web app, TODO multivalued fails?
        'app_status__name',
        ).order_by('release_date', 'acronym', 'release')
    # TODO maybe inject app_class into results since
    # we can't deref by app.app_status__name there?
    return render_to_response('report/app_pipeline_full.html',
                              {'object_list': apps,
                               'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));

def current_dev_by_acronym(request):
    q =     Q(app_status__name__iexact='Current Version') # actual?
    q = q | Q(app_status__name__iexact='In Development')  # projected?
    apps = Application.objects.filter(q).values(
        'id',
        'functional_type__name', # here only,shown as appliation category TODO others too?
        'software_category__name',
        'acronym',
        'app_name',
        'release',
        'app_status__name',
        'release_date',
        'sr_task_order',
        'owner_org',
        'nasa_requester',
        'sr_number',
        # Not used by this template, but in full report
        # 'sr_class__name',
        # 'release_change_description',
        # 'architecture_type',
        ).order_by('acronym', 'release') # diff order than Full pipe
    # TODO maybe inject app_class into results since
    # we can't deref by app.app_status__name there?
    return render_to_response('report/current_dev_by_acronym.html',
                              {'object_list': apps,
                               'search_suggestions': _search_suggestions(),
                               },
                              context_instance=RequestContext(request));
