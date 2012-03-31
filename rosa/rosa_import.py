#!/usr/bin/env python
# Parse the xml with rosa_parse, then walk each app, buld app from attrs, insert into DB

# Dir: /Users/cshenton/Projects/core/rosa/rosa
# export DJANGO_SETTINGS_MODULE=settings
# ./rosa_import.py 

import logging
import json

from django.core.exceptions import ValidationError
from django.db.models.fields import FieldDoesNotExist
from django.db import models

from application.models import Application
from application.models import UNUSED_FIELDS, DATE_FIELDS

logging.basicConfig(level=logging.INFO)

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
    # except ValidationError, e:
    #     logging.error("VALIDATION get_fk model=%s name=%s" % (model, name))
    #     #import pdb; pdb.set_trace()
    #     # cm_resubmit_date like 20120329
    #     # (datefieldobj, model, direct, m2m) = resubdate[0].rel.to._meta.get_field_by_name('name')
    #     # look on that for auto_now_add ? FUGLY
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

model = models.get_model('application', 'Application')

for json_app in json_apps:
    app = Application()
    app.save()                  # save for M2M
    print "app acronym=%s release=%s" % (json_app['acronym'], json_app['release'])
    for k,v in json_app.items():
        if k in UNUSED_FIELDS:
            continue
        if not v:
            continue            # don't bother storing emptiness TODO: Unspecified UNASSIGNE are also empty
        try:
            (field, fmodel, direct, m2m) = dep_field = model._meta.get_field_by_name(k)
        except FieldDoesNotExist, e:
            logging.warning("ERR NOFIELD: %s", e)
        if k in DATE_FIELDS:    # transform DB's 20120330 to 2012-03-30
            v = "%4s-%2s-%2s" % (v[0:4], v[4:6], v[6:8])
        if not field.rel:       # directly attached
            setattr(app, k, v)
        else:
            forn_model =  field.rel.to
            logging.debug("k=%s forn_model=%s" % (k, forn_model))
            if not isinstance(v, list):
                try:
                    setattr(app, k, get_fk(forn_model, v))
                except TypeError, e:
                    logging.error("ERR SETATTR", e)
            else:
                try:
                    vlist = [get_fk(forn_model, vitem) for vitem in v if vitem]
                except ValidationError, e:
                    logging.error("ERR VALIDATION: %s", e) # bad date format??
                    continue
                try:
                    setattr(app, k, vlist)
                except TypeError, e:
                    logging.error("ERR VLIST: %s", e)
                    import pdb; pdb.set_trace()
    app.save()                # Is it not saving the M2M connections?
