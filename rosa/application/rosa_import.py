#!/usr/bin/env python
# Parse the xml with rosa_parse, then walk each app, buld app from attrs, insert into DB

from rosa.application.models import Application, Version, OrganizationalAcronym, TaskOrder, ApplicationType, SoftwareClass, ReleaseStatus

#import rosa_parse

app = Application.object.get(pk=1)
print "App=", app
version = Version(application=app,
                  release_date=isodate(row['release_date']),
                  version_number=row['version_number'],
                  service_request_numbers=row['service_request_numbers'],
                  nasa_owner_office_id=nasa_owner_office_id,
                  nasa_requester=row['nasa_requester'],
                  version_change_description=row['version_change_description'],
                  application_type=application_type,
                  software_class=software_class,
                  version_status=version_status,
                  # These may not be Null, why not?
                  information_sensitivity = get_fk(InformationSensitivity, 'Not In Rosa Report'),
                  authentication_type     = get_fk(AuthenticationMethod,   'Not in Rosa Report'),
                  odin_triage_level       = get_fk(TriageLevel,            'Not in Rosa Report'),
                  user_groups             = get_fk(ApplicationUserGroup,   'Not in Rosa Report'),
                  frequency_used          = get_fk(FrequencyUsed,          'Not in Rosa Report'),
                  architecture_type       = get_fk(ApplicationType,        'Not in Rosa Report'), 
                  )
version.save()


