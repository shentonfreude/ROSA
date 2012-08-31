#!/bin/sh
# Sanitize ROSA data https://github.com/koansys/lorem
# Set your PATH so that lorem.py can be found

DB=rosa/db/rosa.sqlite3

lorem.py sqlite:///${DB} application_application.app_name=text
lorem.py sqlite:///${DB} application_application.app_status_comments=text
lorem.py sqlite:///${DB} application_application.description=text
lorem.py sqlite:///${DB} application_application.dev_name_alternate=name
lorem.py sqlite:///${DB} application_application.dev_name_primary=name
lorem.py sqlite:///${DB} application_application.html_link=url
lorem.py sqlite:///${DB} application_application.manager_app_development=name
lorem.py sqlite:///${DB} application_application.manager_project=name
lorem.py sqlite:///${DB} application_application.nasa_off_name=name
lorem.py sqlite:///${DB} application_application.nasa_requester=name
lorem.py sqlite:///${DB} application_application.owner=name 
lorem.py sqlite:///${DB} application_application.owner_org=number
lorem.py sqlite:///${DB} application_application.owner_org_name=text
lorem.py sqlite:///${DB} application_application.pk_doc_number=number
lorem.py sqlite:///${DB} application_application.release_change_description=text
lorem.py sqlite:///${DB} application_application.release_notes=text
lorem.py sqlite:///${DB} application_application.server_app_name=host
lorem.py sqlite:///${DB} application_application.sr_number=number
lorem.py sqlite:///${DB} application_application.sr_task_order=number

#Don't change acronym or we break all references.
#./lorem.py sqlite:///${DB} application_application.acronym=text

lorem.py sqlite:///${DB} application_gotspoc.name=text # URL or Place/name/phone/email; safest is 'text'
lorem.py sqlite:///${DB} application_location.name=text
lorem.py sqlite:///${DB} application_releaasestatus.name=username # sometimes username: fflintstone
lorem.py sqlite:///${DB} application_secplannumber.name=text
lorem.py sqlite:///${DB} application_securityitcdowner.name=username
lorem.py sqlite:///${DB} application_serverdbname.name=host
lorem.py sqlite:///${DB} application_serverreportname.name=host

