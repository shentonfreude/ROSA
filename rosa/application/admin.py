from django.contrib import admin

from models import Application, Version, Document, Source
from models import ApplicationType, ApplicationUserGroup, AuthenticationMethod, FrequencyUsed, InformationCategory, InformationSensitivity, InterfaceMethod, InterfaceDirection, FunctionalType, OrganizationalAcronym, PrivacyInfoData, ReleaseStatus, SoftwareClass, SupportingNetworkServices, TaskOrder, TriageLevel


admin.site.register(ApplicationType)
admin.site.register(ApplicationUserGroup)
admin.site.register(AuthenticationMethod)
admin.site.register(FrequencyUsed)
admin.site.register(InformationCategory)
admin.site.register(InformationSensitivity)
admin.site.register(InterfaceMethod)
admin.site.register(InterfaceDirection)
admin.site.register(FunctionalType)
admin.site.register(OrganizationalAcronym)
admin.site.register(PrivacyInfoData)
admin.site.register(ReleaseStatus)
admin.site.register(SoftwareClass)
admin.site.register(SupportingNetworkServices)
admin.site.register(TaskOrder)
admin.site.register(TriageLevel)

admin.site.register(Application)
admin.site.register(Version)
admin.site.register(Document)
admin.site.register(Source)
