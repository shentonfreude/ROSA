# Create your views here.
# Fuck, do I really have to make a view for this? 

from django.core.context_processors import csrf
from django.db.models import Q
from django.forms import Form, CharField, DateField, ModelMultipleChoiceField
from django.forms import SelectMultiple

from django.shortcuts import render_to_response
from django.template import RequestContext

import logging
logging.basicConfig(level=logging.DEBUG)

#from models import Project, Center, Status


from csv import DictReader
from models import Application, Version, OrganizationalAcronym, TaskOrder, ApplicationType, SoftwareClass, ReleaseStatus

def csvimport(request):
  csvfile = open("rosa-app-pipeline-full.csv")
  reader = DictReader(csvfile)
  logging.info("fieldnames=%s" % reader.fieldnames)

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

  def get_fk(model, name):
      """Find name in model, if not there, create it. Return key.
      use: get_fk(OrganizationalAcronym, row['nasa_owner_office_id'])
      CAVEAT: this will pollute our DB with useless "Unspecified" and "UNSPECIFIED"
      types of entries. Maybe we can defend against these specific words?
      """
      item = model.objects.filter(name=name)
      logging.info("get_fk model=%s name=%s : item=%s" % (model, name, item))
      if item:
          return model.objects.get(name=name) # this is duplicative, lame
      else:
          item = OrganizationalAcronym(name=name)
          item.save()
          logging.info("get_fk model=%s name=%s : CREATED item=%s" % (model, name, item))
          return item

  for row in reader:
      if not row['release_date']:
          continue
      logging.info("%(release_date)s %(application.acronym)s %(version_number)s %(nasa_owner_office_id)s %(nasa_owner_name)s %(contract_task_order_numbers)s %(application_type)s %(architecture_type)s %(version_status)s" % row)

      logging.info("row: %s" % row)

      app = Application.objects.filter(name=row['application.acronym'])
      if not app:
          app = Application(acronym=row['application.acronym'], name=row['application.name'])
          app.save()

      nasa_owner_office_id              = get_fk(OrganizationalAcronym, row['nasa_owner_office_id'])
      contract_task_order_numbers       = get_fk(TaskOrder,             row['contract_task_order_numbers'])
      application_type                  = get_fk(ApplicationType,       row['application_type'])
      software_class                    = get_fk(SoftwareClass,         row['software_class'])
      version_status                    = get_fk(ReleaseStatus,         row['version_status'])

      logging.info("row fields: nasa_owner_office_id=%s task_order=%s app_type=%s class=%s status=%s" % (
              row['nasa_owner_office_id'],
              row['contract_task_order_numbers'],
              row['application_type'],
              row['software_class'],
              row['version_status']))

      logging.info("fks fields: nasa_owner_office_id=%s task_order=%s app_type=%s class=%s status=%s" % (
              nasa_owner_office_id, contract_task_order_numbers, application_type, software_class, version_status))

      version = Version(application=app,
                        release_date=row['release_date'],
                        version_number=row['version_number'],
                        service_request_numbers=row['service_request_numbers'],
                        nasa_owner_office_id=nasa_owner_office_id,
                        nasa_owner_name=row['nasa_owner_name'],
                        version_change_description=row['version_change_description'],
                        contract_task_order_numbers=contract_task_order_numbers,
                        application_type=application_type,
                        software_class=software_class,
                        version_status=version_status,
                        )
      version.save()




