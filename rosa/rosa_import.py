#!/usr/bin/env python
# Parse the xml with rosa_parse, then walk each app, buld app from attrs, insert into DB

# Dir: /Users/cshenton/Projects/core/rosa/rosa
# export DJANGO_SETTINGS_MODULE=settings
# ./rosa_import.py 

import json
from application.models import Application
from application.models import UNUSED_FIELDS

#import rosa_parse

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

def get_apps_json(json_path):
    return json.loads(file(json_path, 'r').read())

json_apps = get_apps_json("/Users/cshenton/Documents/rosaExportSmall.json")
print "len json_apps=", len(json_apps)

from django.db.models.fields import FieldDoesNotExist
from django.db import models
model = models.get_model('application', 'Application')

for json_app in json_apps:
    app = Application()
    app.save()                  # save for M2M
    print "app acronym=%s release=%s" % (json_app['acronym'], json_app['release'])
    for k,v in json_app.items():
        #print "k=%s v=%s" % (k,v)
        if k in UNUSED_FIELDS:
            continue
        try:
            (field, fmodel, direct, m2m) = dep_field = model._meta.get_field_by_name(k)
        except FieldDoesNotExist, e:
            print "ERR", e
        if not field.rel:       # directly attached
            setattr(app, k, v)
        # except ValueError, e:
        #     print "ERR", e
            
    app.save()                  # save for M2M

# version = Version(application=app,
#                   release_date=isodate(row['release_date']),
#                   version_number=row['version_number'],
#                   service_request_numbers=row['service_request_numbers'],
#                   nasa_owner_office_id=nasa_owner_office_id,
#                   nasa_requester=row['nasa_requester'],
#                   version_change_description=row['version_change_description'],
#                   application_type=application_type,
#                   software_class=software_class,
#                   version_status=version_status,
#                   # These may not be Null, why not?
#                   information_sensitivity = get_fk(InformationSensitivity, 'Not In Rosa Report'),
#                   authentication_type     = get_fk(AuthenticationMethod,   'Not in Rosa Report'),
#                   odin_triage_level       = get_fk(TriageLevel,            'Not in Rosa Report'),
#                   user_groups             = get_fk(ApplicationUserGroup,   'Not in Rosa Report'),
#                   frequency_used          = get_fk(FrequencyUsed,          'Not in Rosa Report'),
#                   architecture_type       = get_fk(ApplicationType,        'Not in Rosa Report'), 
#                   )
# version.save()


