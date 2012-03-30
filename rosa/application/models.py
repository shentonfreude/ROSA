from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, ManyToManyField
from django.db.models import NullBooleanField, CharField, DateField, EmailField, IntegerField, TextField

# TODO: make these key tables UNIQ

# TODO: we shouldn't allow Null or Empty names?

class AppStatus(Model):              # M2M
    name = CharField(max_length=64, blank=True) ##Archived, Cancelled, Current Version, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class AppType(Model):              # M2M
    name = CharField(max_length=64, blank=True) ##Application, General Support System, Major Application, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class AppUsage(Model):             # M2M
    name = CharField(max_length=64, blank=True) ##Agency-Wide, HQ-Wide, Multiple Org, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class ArchitectureType(Model):     # M2M
    name = CharField(max_length=64, blank=True) ##C/S, C/S and Web App, M/F, Web App, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class AuthenticationType(Model):   # M2M
    name = CharField(max_length=64, blank=True) ##Active Directory, ID/PW Only, ID/PW and Token, ...
    def __unicode__(self):
        return u'%s' % (self.name)

class BiaCategory(Model):          # FK
    name = CharField(max_length=64, blank=True) ## ['High', 'Low', 'Moderate', 'Not Applicable', 'Unassigned']
    def __unicode__(self):
        return u'%s' % (self.name)

class BrowserSupport(Model):       # M2M
    name = CharField(max_length=64, blank=True) ##IE, MOZILLA, Mozilla, STANDARD WEB BROWSER
    def __unicode__(self):
        return u'%s' % (self.name)

class CmResubmitDate(Model):       # M2M
    name = DateField(blank=True, null=True) #
    def __unicode__(self):
        return u'%s' % (self.name)

class DbmsName(Model):       # M2M
    name = CharField(max_length=64, blank=True) #
    def __unicode__(self):
        return u'%s' % (self.name)

class FipsInfoCategory(Model):     # FK
    name = CharField(max_length=64, blank=True) ## ['Low', 'Medium', 'Moderate', 'Moderate: D.20.1, C.3.5.1'...]
    def __unicode__(self):
        return u'%s' % (self.name)

class Frequency(Model):            # FK
    name = CharField(max_length=64, blank=True) ## ['ANNUALLY', 'AS NEEDED','DAILY', 'Monthly'...]
    def __unicode__(self):
        return u'%s' % (self.name)

class FunctionalType(Model):       # M2M
    name = CharField(max_length=64, blank=True) ##Acct,Budget,DMS,Finance,GENERAL ADMIN
    def __unicode__(self):
        return u'%s' % (self.name)

class GotsPoc(Model):              # FK
    name = CharField(max_length=64, blank=True) ## ['Beverly Smith', 'DCAA', 'DOI NBC', ...]
    def __unicode__(self):
        return u'%s' % (self.name)

class InternalSystem(Model):       # FK
    name = CharField(max_length=64, blank=True) ## [None, 'E', 'I', 'Not Applicable', 'Unassigned']
    def __unicode__(self):
        return u'%s' % (self.name)

class Location(Model):             # M2M
    name = CharField(max_length=64, blank=True) ##GSFC,MSFC,NACC-CPO,NASA HQ Hosted,NASA Portal,...
    def __unicode__(self):
        return u'%s' % (self.name)

class ManagedRecords(Model):       # FK
    name = CharField(max_length=64, blank=True) ## [None, 'C', 'CS', 'Unassigned']
    def __unicode__(self):
        return u'%s' % (self.name)

class NetworkServicesUsed(Model):  # M2M
    name = CharField(max_length=64, blank=True) ##Extranet,Intranet
    def __unicode__(self):
        return u'%s' % (self.name)

class ReleaseStatus(Model):        # FK
    name = CharField(max_length=64, blank=True) ## ['Unknown', 'hgoetzel', 'tmshelto', 'tshelton']
    def __unicode__(self):
        return u'%s' % (self.name)

class SecPlanNumber(Model):        # FK
    name = CharField(max_length=64, blank=True) ## [' 20090812', '0A-801-M-NHQ-0001', '20090812',...]
    def __unicode__(self):
        return u'%s' % (self.name)

class Section2810Compliant(Model): # FK
    name = CharField(max_length=64, blank=True) ## ['No', 'Not Applicable', 'Partial', 'Unassigned', 'Yes']
    def __unicode__(self):
        return u'%s' % (self.name)

class SecurityItcdOwner(Model):    # FK
    name = CharField(max_length=64, blank=True, null=True) ## ['ANDREW BONCEK', 'ANDY BONCEK', 'Andrew Boncek',...]
    def __unicode__(self):
        return u'%s' % (self.name)

class SecurityPiiIndicator(Model): # M2M
    name = CharField(max_length=64, blank=True) ##TOO MANY=51
    def __unicode__(self):
        return u'%s' % (self.name)

class SecuritySensitivity(Model):  # FK
    name = CharField(max_length=64, blank=True) ## [BIA info Category = ADM-Administrative','FOIA Exempt',...]
    def __unicode__(self):
        return u'%s' % (self.name)

class ServerDbName(Model):         # M2M
    name = CharField(max_length=64, blank=True) ##TOO MANY=81
    def __unicode__(self):
        return u'%s' % (self.name)

class ServerReportName(Model):     # FK
    name = CharField(max_length=64, blank=True) ## ['CASPIAN', 'DRAGONOV', 'HQDATA1 Server', ...]
    def __unicode__(self):
        return u'%s' % (self.name)

class SoftwareCategory(Model):     # M2M
    name = CharField(max_length=64, blank=True) ##A,B,C,D,E,F,G,H
    def __unicode__(self):
        return u'%s' % (self.name)

class Sorn(Model):                 # FK
    name = CharField(max_length=64, blank=True) ## ['10SECR', 'In Draft', 'Schedule 9, 9000.3',...]
    def __unicode__(self):
        return u'%s' % (self.name)

class SrClass(Model):              # M2M
    name = CharField(max_length=64, blank=True) ##1,2
    def __unicode__(self):
        return u'%s' % (self.name)

class SupportStatus(Model):        # M2M
    name = CharField(max_length=64, blank=True) ##COTS,CUSTOM,Custom,GOTS,MOTS
    def __unicode__(self):
        return u'%s' % (self.name)

class SwLanguage(Model):           # M2M
    name = CharField(max_length=64, blank=True) ##TOO MANY=827
    def __unicode__(self):
        return u'%s' % (self.name)

class TriageLevel(Model):          # FK
    name = CharField(max_length=64, blank=True) ## ['Call List', 'Triage 2', 'Triage 3', 'Unassigned']
    def __unicode__(self):
        return u'%s' % (self.name)


#####

# People should be FKs to, so we don't misspell Andrew/ANDREW/Andy Bonceck/BONCEK

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

# We're not having separate Application and Version objects:
# almost every field can change, version to version.
# In ROSA, even the Description is changed from 1.0 to 2.5.3.

class Application(Model):
    acronym                     = CharField(max_length=128)
    acronym_inter_direction     = CharField(max_length=128, blank=True, null=True) # TOO MANY: 39
    acronym_inter_method        = CharField(max_length=128, blank=True, null=True) # TOO MANY: 44
    acronym_interface           = CharField(max_length=128, blank=True, null=True) # TOO MANY: 325
    acronymrelease              = CharField(max_length=128, blank=True, null=True) # DUPES acronym + release "PAVE 2.5.3"
    app_name                    = CharField(max_length=128) # Providing Advanced Visibilty Effort
    app_status                  = ManyToManyField(AppStatus, blank=True, null=True) #Archived, Cancelled, Current Version, ... HOW CAN THIS BE M2M???
    app_status_comments         = CharField(max_length=128, blank=True, null=True) # TOO MANY: 413
    app_type                    = ManyToManyField(AppType, blank=True, null=True) #Application, General Support System, Major Application, ...
    app_usage                   = ManyToManyField(AppUsage, blank=True, null=True) #Agency-Wide, HQ-Wide, Multiple Org, ...
    app_users_num               = CharField(max_length=128, blank=True, null=True) # TOO MANY: 120
    architecture_type           = ManyToManyField(ArchitectureType, blank=True, null=True) #C/S, C/S and Web App, M/F, Web App, ...
    authentication_type         = ManyToManyField(AuthenticationType, blank=True, null=True) #Active Directory, ID/PW Only, ID/PW and Token, ...
    awrs_checklist              = NullBooleanField(blank=True, null=True) 
    awrs_indicator              = NullBooleanField(blank=True, null=True)
    bia_category                = ForeignKey(BiaCategory, blank=True, null=True) # ['High', 'Low', 'Moderate', 'Not Applicable', 'Unassigned']
    browser_support             = ManyToManyField(BrowserSupport, blank=True, null=True) #IE, MOZILLA, Mozilla, STANDARD WEB BROWSER
    cm_entered_time             = CharField(max_length=128, blank=True, null=True) # TOO MANY: 2511 -- TODO TimeField?
    cm_resubmit_date            = ManyToManyField(CmResubmitDate, blank=True, null=True) # TOO MANY: 297  -- TODO DateField
    dbms_name                   = ManyToManyField(DbmsName, blank=True, null=True) #TOO MANY=104
    description                 = CharField(max_length=128, blank=True, null=True) # TOO MANY: 1162
    dev_name_alternate          = CharField(max_length=128, blank=True, null=True) # TOO MANY: 229
    dev_name_primary            = CharField(max_length=128, blank=True, null=True) # TOO MANY: 253
    fed_record_qualification    = NullBooleanField(blank=True, null=True)
    fed_registy                 = NullBooleanField(blank=True, null=True)
    fips_info_category          = ForeignKey(FipsInfoCategory, blank=True, null=True) # ['Low', 'Medium', 'Moderate', 'Moderate: D.20.1, C.3.5.1'...]
    firewall_factor             = NullBooleanField(blank=True, null=True)
    frequency                   = ForeignKey(Frequency, blank=True, null=True) # ['ANNUALLY', 'AS NEEDED','DAILY', 'Monthly'...]
    functional_type             = ManyToManyField(FunctionalType, blank=True, null=True) #Acct,Budget,DMS,Finance,GENERAL ADMIN
    gots_poc                    = ForeignKey(GotsPoc, blank=True, null=True) # ['Beverly Smith', 'DCAA', 'DOI NBC', ...]
    hitss_supported             = NullBooleanField(blank=True, null=True)
    html_link                   = CharField(max_length=128, blank=True, null=True) # TOO MANY: 558
    internal_system             = ForeignKey(InternalSystem, blank=True, null=True) # [None, 'E', 'I', 'Not Applicable', 'Unassigned']
    location                    = ManyToManyField(Location, blank=True, null=True) #GSFC,MSFC,NACC-CPO,NASA HQ Hosted,NASA Portal,...
    managed_records             = ForeignKey(ManagedRecords, blank=True, null=True) # [None, 'C', 'CS', 'Unassigned']
    manager_app_development     = CharField(max_length=128, blank=True, null=True) # TOO MANY: 67
    manager_project             = CharField(max_length=128, blank=True, null=True) # TOO MANY: 106
    nasa_off_name               = CharField(max_length=128, blank=True, null=True) # TOO MANY: 75
    nasa_requester              = CharField(max_length=128, blank=True, null=True) # TOO MANY: 554
    network_services_used       = ManyToManyField(NetworkServicesUsed, blank=True, null=True) #Extranet,Intranet
    nrrs_disposition            = NullBooleanField(blank=True, null=True)
    nrrs_schedule_item          = CharField(max_length=128, blank=True, null=True) # TOO MANY: 56
    owner                       = CharField(max_length=128, blank=True, null=True) # TOO MANY: 472
    owner_org                   = CharField(max_length=128, blank=True, null=True) # TOO MANY: 305
    owner_org_name              = CharField(max_length=128, blank=True, null=True) # TOO MANY: 454
    pk_doc_number               = CharField(max_length=128, blank=True, null=True) # TOO MANY: 2523
    privacy_act                 = NullBooleanField(blank=True, null=True)
    re_entered_time             = CharField(max_length=128, blank=True, null=True) # TOO MANY: 1269
    release                     = CharField(max_length=128) # 2.5.3
    release_change_description  = CharField(max_length=128, blank=True, null=True) # TOO MANY: 1684
    release_date                = CharField(max_length=128, blank=True, null=True) # TOO MANY: 1457 TODO DateField
    release_notes               = CharField(max_length=128, blank=True, null=True) # TOO MANY: 220
    release_status              = ForeignKey(ReleaseStatus, blank=True, null=True) # ['Unknown', 'hgoetzel', 'tmshelto', 'tshelton']
    sec_plan_number             = ForeignKey(SecPlanNumber, blank=True, null=True) # [' 20090812', '0A-801-M-NHQ-0001', '20090812',...]
    section2810compliant        = ForeignKey(Section2810Compliant, blank=True, null=True) # ['No', 'Not Applicable', 'Partial', 'Unassigned', 'Yes']
    section508complaint         = NullBooleanField(blank=True, null=True)
    security_itcd_owner         = ForeignKey(SecurityItcdOwner, blank=True, null=True) # ['ANDREW BONCEK', 'ANDY BONCEK', 'Andrew Boncek',...]
    security_pii_indicator      = NullBooleanField(blank=True, null=True)
    security_pii_type           = ManyToManyField(SecurityPiiIndicator, blank=True, null=True) #TOO MANY=51
    security_sensitivity        = ForeignKey(SecuritySensitivity, blank=True, null=True) # [BIA info Category = ADM-Administrative','FOIA Exempt',...]
    server_app_name             = CharField(max_length=128, blank=True, null=True) # TOO MANY: 122
    server_db_name              = ManyToManyField(ServerDbName, blank=True, null=True) #TOO MANY=81
    server_report_name          = ForeignKey(ServerReportName, blank=True, null=True) # ['CASPIAN', 'DRAGONOV', 'HQDATA1 Server', ...]
    software_category           = ManyToManyField(SoftwareCategory, blank=True, null=True) #A,B,C,D,E,F,G,H
    sorn                        = ForeignKey(Sorn, blank=True, null=True) # ['10SECR', 'In Draft', 'Schedule 9, 9000.3',...]
    sr_class                    = ManyToManyField(SrClass, blank=True, null=True) #1,2
    sr_number                   = CharField(max_length=128, blank=True, null=True) # TOO MANY: 1963
    sr_task_order               = CharField(max_length=128, blank=True, null=True) # TOO MANY: 78
    ssn_system                  = NullBooleanField(blank=True, null=True)
    support_status              = ManyToManyField(SupportStatus, blank=True, null=True) #COTS,CUSTOM,Custom,GOTS,MOTS
    sw_language                 = ManyToManyField(SwLanguage, blank=True, null=True) #TOO MANY=827
    triage_level                = ForeignKey(TriageLevel, blank=True, null=True) # ['Call List', 'Triage 2', 'Triage 3', 'Unassigned']

    def __unicode__(self):
        return u'%s-%s' % (self.acronym, self.release)


# class Document(Model):
#     pass

# class Source(Model):
#     # source code files
#     pass

