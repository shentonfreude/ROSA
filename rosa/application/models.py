from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, ManyToManyField
from django.db.models import BooleanField, CharField, DateField, EmailField, IntegerField, TextField

# TODO: make these key tables UNIQ

class ApplicationType(Model):
    name = CharField(max_length=32, blank=True) #c/s, webapp, web site
    def __unicode__(self):
        return u'%s' % (self.name)

class ApplicationUserGroup(Model):
    name = CharField(max_length=32, blank=True) #agency, hq, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class AuthenticationMethod(Model):
    name = CharField(max_length=32, blank=True) #id/pw, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class FrequencyUsed(Model):
    name = CharField(max_length=32, blank=True) #daily, weekly
    def __unicode__(self):
        return u'%s' % (self.name)

class InformationCategory(Model):
    name = CharField(max_length=32, blank=True) #auto, manual
    def __unicode__(self):
        return u'%s' % (self.name)

class InformationSensitivity(Model):
    name = CharField(max_length=32, blank=True) #FOIA Exempt, low, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class InterfaceMethod(Model):                    # multiple, for diff interfaces??
    name = CharField(max_length=32, blank=True) #auto, manual
    def __unicode__(self):
        return u'%s' % (self.name)

class InterfaceDirection(Model):                    # multiple, for diff interfaces??
    name = CharField(max_length=32, blank=True) #pull, push
    def __unicode__(self):
        return u'%s' % (self.name)

class FunctionalType(Model):
    name = CharField(max_length=32, blank=True) #dms, general...
    def __unicode__(self):
        return u'%s' % (self.name)

class OrganizationalAcronym(Model):
    name = CharField(max_length=32, blank=True)
    def __unicode__(self):
        return u'%s' % (self.name)

class PrivacyInfoData(Model):
    name = CharField(max_length=32, blank=True) # Name, Adress...
    def __unicode__(self):
        return u'%s' % (self.name)

class ReleaseStatus(Model):
    name = CharField(max_length=32, blank=True) # Current Version, In Development
    def __unicode__(self):
        return u'%s' % (self.name)

class SoftwareClass(Model):
    name = CharField(max_length=32, blank=True) # D,F,G,H
    def __unicode__(self):
        return u'%s' % (self.name)

class SupportingNetworkServices(Model):
    name = CharField(max_length=32, blank=True) # Extranet, Intranet
    def __unicode__(self):
        return u'%s' % (self.name)

class TaskOrder(Model):
    name = CharField(max_length=32, blank=True) # 10.99
    def __unicode__(self):
        return u'%s' % (self.name)

class TriageLevel(Model):
    name = CharField(max_length=32, blank=True) # Call List, 2, 3
    def __unicode__(self):
        return u'%s' % (self.name)



# Almost every field can change, version to version.
# In ROSA, even the Description is changed from 1.0 to 2.5.3.

class Application(Model):
    acronym = CharField(max_length=128)
    current_version = ForeignKey('Version', related_name='current_version', blank=True, null=True)
    name = CharField(max_length=128)
    description = CharField(max_length=128)

    def __unicode__(self):
        return u'%s' % (self.acronym)

# Fields below broken down by report form clustering
class Version(Model):
    # Application
    application = ForeignKey(Application, related_name='application')
    #name
    #description
    nasa_owner_name = CharField(max_length=128, blank=True)
    functional_types = ManyToManyField(FunctionalType, blank=True)
    nasa_analyst_name = CharField(max_length=128, blank=True)
    software_class = ForeignKey(SoftwareClass, blank=True)
    # Release/Configuration
    version_status = ForeignKey(ReleaseStatus)
    version_number = CharField(max_length=128)
    version_change_description = TextField(max_length=2048, blank=True)
    release_date = DateField(max_length=128, blank=True)
    service_request_numbers = CharField(max_length=128, blank=True)
    # Security/Compliance
    application_type = ForeignKey(ApplicationType, blank=True, null=True, related_name="application_type")
    fips_information_category = ForeignKey(InformationCategory, blank=True, null=True)
    information_sensitivity = ForeignKey(InformationSensitivity, blank=True, null=True) # add Nullable needed?
    authentication_type = ForeignKey(AuthenticationMethod, blank=True)
    privacy_info_indicator = BooleanField(blank=True)
    privacy_info_data_types = ManyToManyField(PrivacyInfoData, blank=True)
    compliance_2810 = BooleanField(blank=True)
    compliance_508 = BooleanField(blank=True)
    compliance_awrs = BooleanField(blank=True)
    # Organizational/Support Team
    nasa_owner_organization_name = CharField(max_length=128, blank=True)
    nasa_owner_office_id = ForeignKey(OrganizationalAcronym)
    nasa_requester = CharField(max_length=128)
    contract_task_order_numbers = ManyToManyField(TaskOrder, blank=True)
    odin_triage_level = ForeignKey(TriageLevel, blank=True)
    branch_manager_name = CharField(max_length=128, blank=True)
    project_manager_name = CharField(max_length=128, blank=True)
    developer_primary = CharField(max_length=128)
    developer_alternate = CharField(max_length=128, blank=True)
    # Usage/Frequency
    user_groups = ForeignKey(ApplicationUserGroup, blank=True)
    frequency_used = ForeignKey(FrequencyUsed, blank=True)
    number_of_users = IntegerField(blank=True, null=True) # new null
    # Architecture
    architecture_type = ForeignKey(ApplicationType, blank=True) # WRONG, this dupes application_type above?
    url_link = CharField(max_length=128, blank=True)
    dbms_names_and_version = CharField(max_length=128, blank=True)
    software_names_and_versions = CharField(max_length=256, blank=True)
    #todo: make these M2M fields so they can be added thru the ui
    servers_application = CharField(max_length=128, blank=True)
    servers_database = CharField(max_length=128, blank=True)
    servers_report = CharField(max_length=128, blank=True)
    network_services_used = ManyToManyField(SupportingNetworkServices, blank=True)
    # Interface/Shared Dependencies
    interface_acronym = ManyToManyField(Application, blank=True) # circular reference
    interface_direction = ManyToManyField(InterfaceDirection, blank=True, null=True)
    interface_method = ManyToManyField(InterfaceMethod, blank=True)
    federal_records_qualification = CharField(max_length=128, blank=True)
    nrrs_disposition = CharField(max_length=128, blank=True)
    nrrs_schedule_item = CharField(max_length=128, blank=True)
    # NOT IN THE REPORT?:
    support_class = CharField(max_length=128, blank=True) # should be fk?
    servers_location = CharField(max_length=128, blank=True)
    disposition_comments = CharField(max_length=128, blank=True)
    release_notes = CharField(max_length=128, blank=True)
    service_request_classes = CharField(max_length=128, blank=True)
    hitss_supported = CharField(max_length=128, blank=True)
    gots_agency_contact_information = CharField(max_length=128, blank=True)
    data_impact_type = CharField(max_length=128, blank=True)
    privacy_act_system = CharField(max_length=128, blank=True)
    awrs_check_list_on_file = CharField(max_length=128, blank=True)
    itcd_security_owner_name = CharField(max_length=128, blank=True)
    firewall_w2_factor_token_authentication = CharField(max_length=128, blank=True)
    contractor_civil_servant_managed_records = CharField(max_length=128, blank=True)
    ssn_system = CharField(max_length=128, blank=True)
    filed_with_federal_registry = CharField(max_length=128, blank=True)
    internal_or_external_system = CharField(max_length=128, blank=True)
    sorn_system_of_records_notice_number = CharField(max_length=128, blank=True)
    security_plan_number = CharField(max_length=128, blank=True)
    web_browsers = CharField(max_length=128, blank=True)

    def __unicode__(self):
        return u'%s-%s' % (self.application.acronym, self.version_number)


class Document(Model):
    pass

class Source(Model):
    # source code files
    pass

