from django.contrib import admin

from models import AppStatus
from models import AppType
from models import AppUsage
from models import ArchitectureType
from models import AuthenticationType
from models import BiaCategory
from models import BrowserSupport
from models import CmResubmitDate
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
admin.site.register(CmResubmitDate)
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
admin.site.register(Application)
#admin.site.register(Document)
#admin.site.register(Source)

