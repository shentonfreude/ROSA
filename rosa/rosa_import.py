#!/usr/bin/env python
# Parse the xml with rosa_parse, then walk each app, buld app from attrs, insert into DB

# Dir: /Users/cshenton/Projects/core/rosa/rosa
# export DJANGO_SETTINGS_MODULE=settings
# ./rosa_import.py 

# TODO: 
# SlugField: acronym-release
# ERR INTEGER k=app_users_num v=Web Site (storing 0)
# ERR INTEGER k=app_users_num v=Public (storing 0)
# - get_fk model=<class 'application.models.DbmsName'> name=Not Applicable : CREATED item=Not Applicable
# - get_fk model=<class 'application.models.SoftwareCategory'> name=Not Applicable : CREATED item=Not Applicable
# - get_fk model=<class 'application.models.ArchitectureType'> name=Not Applicable : CREATED item=Not Applicable

import logging
import json
import sys

from django.core.exceptions import ValidationError
from django.db.models.fields import FieldDoesNotExist
from django.db import models

from application.models import Application

logging.basicConfig(level=logging.INFO)

if len(sys.argv) != 2:
    raise RuntimeError("Specify rosaExport.json file path as argument")
JSON_FILE = sys.argv[1]

UNUSED_FIELDS = (               # Never populated in Rosa export
    'acronym_inter_notes',
    'app_doc_type',
    'bia_assesment',
    'capcity_requirement',
    'data_owner',
    'date_holder',
    'date_holder2',
    'dbms_type',
    'holder1',
    'holder2',
    'holder3',
    'hw_support',
    'internet_zone',
    'os_name',
    'os_support',
    'pvcs_created_date',
    'record_retention_number',
    'relocation_center',
    'security_impact',
    'security_info_category',
    'source_code_location',
    'source_code_location_comment',
    'archive_code',         # 460 are '0', 2098 are empty
    'gots_agency_info'      # all empty but 1 'Jason Bollinger 321-867-4334'
    'migration_id',         # 2558 are always '1'
    'orgcode',              # all 2558 are 'A'
    'sw_tools',             # all empty but 1 'Dreamweaver'
    # Other crap fields we found on insert
    'combined_search',
    'userlevel',
    'migration_id',
    'gots_agency_info',
    'doclevel',
    'software_category_all',
    'location_all',
    'filename',
    'version_version_number',
    'acronym_inter_direction_all',
    'sr_number_all',
    'group_code',
    'bia_category_all',
    'requests',
    'cm_entered_date',
    'app_type_all',
    'entered_date',
    'access_history',
    're_entered_date',
    'syskey',
    'architecture_type_all',
    'doc_number',
    'server_db_name_all',
    'icon',
    'version_highest_version_flag',
    )

NULLISH_VALUES = (
    None,
    [],
    '',
    'Unassigned',
    'Unk',
    'Unknown',
    'Not Applicable',
)

DATE_FIELDS = ('release_date', 'cm_resubmit_date') # have to transform on load

TIME_FIELDS = ('cm_entered_time', 're_entered_time') # have to transform on load

INTEGER_FIELDS = ('app_users_num',)

BOOLEAN_FIELDS = (
    'awrs_checklist',
    'awrs_indicator',
    'fed_record_qualification',
    'fed_registry',
    'firewall_factor',
    'hitss_supported',
    'nrrs_disposition',
    'privacy_act',
    'section508compliant',
    'security_pii_indicator',
    'ssn_system',
    )

def _booleanize(val):
    """Return True/False based on text.
    """
    return val.lower in ('yes', 'true', 'y')

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
        logging.info("CREATE model=%s name=%s" % (model, name))
    return item


def get_apps_json(json_path):
    return json.loads(file(json_path, 'r').read())

json_apps = get_apps_json(JSON_FILE)
print "len json_apps=", len(json_apps)

model = models.get_model('application', 'Application')

# TODO: Are (Null)Boolean fields saved properly?
# TODO: cm_resubmit_{date,time} fields to single DateTime

total_apps = len(json_apps)
logging.info("TOTAL APPS=%d" % total_apps)
num_apps = 0
for json_app in json_apps:
    num_apps += 1
    app = Application()
    app.save()                  # save for M2M
    logging.info("APP %d %d%%: %s %s" % (
            num_apps, int(100 * num_apps / total_apps),
            json_app['acronym'], json_app['release']))
    for k,v in json_app.items(): # Do we need to strip values?
        # Skip junk
        if k in UNUSED_FIELDS:
            continue
        if isinstance(v, list): # filter Nulls from M2M lists
            v = [vv for vv in v if not v in NULLISH_VALUES]
        if v in NULLISH_VALUES: # Don't bother storing empty data
            #logging.info("NULL k=%s v=%s" % (k,v))
            continue
        if not v:               # Don't bother storing empty data or list
            continue
        try:
            (field, fmodel, direct, m2m) = dep_field = model._meta.get_field_by_name(k)
        except FieldDoesNotExist, e:
            logging.warning("ERR NOFIELD: %s", e)

        # Transform
        if k in DATE_FIELDS:    # transform DB's 20120330 to 2012-03-30
            v = "%4s-%2s-%2s" % (v[0:4], v[4:6], v[6:8])
            #logging.info("DATE k=%s v=%s" % (k,v))
        elif k in TIME_FIELDS:
            # OMFG times shaped like "145859" and 5-digit "95355".
            # Found SIERA-1.4  with 4-digits "4153", how to interpret?
            # Found NCTS-2.7.1 with 4-digits "4111", how to interpret?
            v = "0" * (6 - len(v)) + v # leading zero-pad
            v = "%2s:%2s:%2s" % (v[0:2], v[2:4], v[4:6])
            #logging.info("TIME k=%s v=%s" % (k,v))
        elif k in BOOLEAN_FIELDS:
            #logging.info("BOOL k=%s v=%s bool=%s" % (k,v, (v.lower() in ('yes', 'true', 'y'))))
            v = (v.lower() in ('yes', 'true', 'y'))
        elif k in INTEGER_FIELDS:
            try:
                v = int(v.replace(',', '')) # 2,000 -> 2000
            except ValueError, e:
                logging.warning("ERR INTEGER k=%s v=%s (storing None)" % (k,v))
                v = None

        # Save as Field, FK, or M2M
        try:
            if not field.rel:       # directly attached
                setattr(app, k, v)
            else:
                forn_model =  field.rel.to
                logging.debug("k=%s forn_model=%s" % (k, forn_model))
                if not isinstance(v, list): # FK
                    setattr(app, k, get_fk(forn_model, v))
                else:               # M2M so make list of FKs
                    vlist = [get_fk(forn_model, vitem) for vitem in v if vitem]
                    setattr(app, k, vlist)
        except (TypeError, ValidationError), e:
            logging.error("SETATTR: %s", e)
            import pdb; pdb.set_trace()

    try:
        app.save()                # Is it not saving the M2M connections?
    except (TypeError, ValidationError), e:
        logging.error("SAVE SETATTR: %s", e)
        import pdb; pdb.set_trace()

