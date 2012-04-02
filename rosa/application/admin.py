from django.contrib import admin

from models import AppStatus
from models import AppType
from models import AppUsage
from models import ArchitectureType
from models import AuthenticationType
from models import BiaCategory
from models import BrowserSupport
from models import FipsInfoCategory
from models import Frequency
from models import FunctionalType
from models import GotsPoc
from models import InternalSystem
from models import Location
from models import ManagedRecords
from models import NetworkServicesUsed
from models import ReleaseStatus
from models import SecPlanNumber
from models import Section2810Compliant
from models import SecurityItcdOwner
from models import SecurityPiiIndicator
from models import SecuritySensitivity
from models import ServerDbName
from models import ServerReportName
from models import SoftwareCategory
from models import Sorn
from models import SrClass
from models import SupportStatus
from models import SwLanguage
from models import TriageLevel
from models import Application
#from models import Document
#from models import Source


admin.site.register(AppStatus)
admin.site.register(AppType)
admin.site.register(AppUsage)
admin.site.register(ArchitectureType)
admin.site.register(AuthenticationType)
admin.site.register(BiaCategory)
admin.site.register(BrowserSupport)
admin.site.register(FipsInfoCategory)
admin.site.register(Frequency)
admin.site.register(FunctionalType)
admin.site.register(GotsPoc)
admin.site.register(InternalSystem)
admin.site.register(Location)
admin.site.register(ManagedRecords)
admin.site.register(NetworkServicesUsed)
admin.site.register(ReleaseStatus)
admin.site.register(SecPlanNumber)
admin.site.register(Section2810Compliant)
admin.site.register(SecurityItcdOwner)
admin.site.register(SecurityPiiIndicator)
admin.site.register(SecuritySensitivity)
admin.site.register(ServerDbName)
admin.site.register(ServerReportName)
admin.site.register(SoftwareCategory)
admin.site.register(Sorn)
admin.site.register(SrClass)
admin.site.register(SupportStatus)
admin.site.register(SwLanguage)
admin.site.register(TriageLevel)
#admin.site.register(Document)
#admin.site.register(Source)

class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Essential',   {'fields': ('acronym',
                                    'app_name',
                                    'release')
                         }),
        ('Vitals',      {'fields' : ('app_status',
                                     'release_date',
                                     'release_status')
                         }),
        ('Overview',    {'fields': ('description',
                                    'release_change_description',
                                    'release_notes'),
                         'classes': ('collapse',)
                         }),
        ('Details', {'fields': ('app_status_comments',
                                'functional_type',
                                'app_type',
                                'software_category',
                                'architecture_type',
                                'app_usage',
                                'app_users_num',
                                'frequency',
                                'browser_support',
                                'html_link',
                                'support_status',
                                'sw_language',
                                'triage_level'),
                     'classes': ('collapse',)
                     }),
        ('Personnel', {'fields': ('owner',
                                  'owner_org',
                                  'owner_org_name',
                                  'nasa_off_name',
                                  'nasa_requester',
                                  'gots_poc',
                                  'manager_app_development',
                                  'manager_project',
                                  'managed_records',
                                  'dev_name_primary',
                                  'dev_name_alternate'),
                       'classes': ('collapse',)
                       }),

        ('Systems',     {'fields': ('internal_system',
                                    'location',
                                    'dbms_name',
                                    'network_services_used',
                                    'server_app_name',
                                    'server_db_name',
                                    'server_report_name',
                                    ),
                         'classes': ('collapse',)
                         }),
        ('Interfaces',  {'fields': ('acronym_interface',
                                    'acronym_inter_direction',
                                    'acronym_inter_method',
                                    ),
                         'classes': ('collapse',)
                         }),
        ('Security',    {'fields': ('security_itcd_owner',
                                    'security_pii_indicator',
                                    'security_pii_type',
                                    'security_sensitivity',
                                    'authentication_type',
                                    'bia_category',
                                    'fips_info_category',
                                    'firewall_factor',
                                    'privacy_act',
                                    'sec_plan_number',
                                    'ssn_system',
                                    ),
                         'classes': ('collapse',)
                         }),
        ('Certification',       {'fields': ('awrs_checklist',
                                            'awrs_indicator',
                                            'fed_record_qualification',
                                            'fed_registy',
                                            'hitss_supported',
                                            'section2810compliant',
                                            'section508complaint',
                                            ),
                                 'classes': ('collapse',)
                                 }),
        ('Process',             {'fields': ('sr_class',
                                            'sr_number',
                                            'sr_task_order',
                                            'cm_resubmit_date',
                                            'cm_entered_time',
                                            're_entered_time',
                                            ),
                                 'classes': ('collapse',)
                                 }),
        ('TBD',                 {'fields': ('nrrs_disposition',
                                            'nrrs_schedule_item',
                                            'pk_doc_number',
                                            'sorn',
                                            ),
                                 'classes': ('collapse',)
                                 }),
        )


admin.site.register(Application, ApplicationAdmin)
