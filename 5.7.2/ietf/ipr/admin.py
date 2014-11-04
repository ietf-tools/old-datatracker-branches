#coding: utf-8
from django.contrib import admin
from ietf.ipr.models import IprNotification, IprDisclosureBase, IprDocRel, IprEvent, RelatedIpr, HolderIprDisclosure, ThirdPartyIprDisclosure, GenericIprDisclosure, NonDocSpecificIprDisclosure

# ------------------------------------------------------
# ModelAdmins
# ------------------------------------------------------
class IprDisclosureBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_date', 'related_docs', 'state']
    search_fields = ['title', 'legal_name']
    
    def related_docs(self, obj):
        return u", ".join(a.formatted_name() for a in IprDocRel.objects.filter(disclosure=obj).order_by("id").select_related("document"))

admin.site.register(IprDisclosureBase, IprDisclosureBaseAdmin)

class HolderIprDisclosureAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_date', 'related_docs', 'state']
    raw_id_fields = ["by"]
    
    def related_docs(self, obj):
        return u", ".join(a.formatted_name() for a in IprDocRel.objects.filter(disclosure=obj).order_by("id").select_related("document"))

admin.site.register(HolderIprDisclosure, HolderIprDisclosureAdmin)

class ThirdPartyIprDisclosureAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_date', 'related_docs', 'state']
    raw_id_fields = ["by"]
    
    def related_docs(self, obj):
        return u", ".join(a.formatted_name() for a in IprDocRel.objects.filter(disclosure=obj).order_by("id").select_related("document"))

admin.site.register(ThirdPartyIprDisclosure, ThirdPartyIprDisclosureAdmin)

class GenericIprDisclosureAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_date', 'related_docs', 'state']
    raw_id_fields = ["by"]
    
    def related_docs(self, obj):
        return u", ".join(a.formatted_name() for a in IprDocRel.objects.filter(disclosure=obj).order_by("id").select_related("document"))

admin.site.register(GenericIprDisclosure, GenericIprDisclosureAdmin)

class NonDocSpecificIprDisclosureAdmin(admin.ModelAdmin):
    list_display = ['title', 'submitted_date', 'related_docs', 'state']
    raw_id_fields = ["by"]
    
    def related_docs(self, obj):
        return u", ".join(a.formatted_name() for a in IprDocRel.objects.filter(disclosure=obj).order_by("id").select_related("document"))

admin.site.register(NonDocSpecificIprDisclosure, NonDocSpecificIprDisclosureAdmin)

class IprNotificationAdmin(admin.ModelAdmin):
    pass
admin.site.register(IprNotification, IprNotificationAdmin)

class IprDocRelAdmin(admin.ModelAdmin):
    raw_id_fields = ["disclosure", "document"]
admin.site.register(IprDocRel, IprDocRelAdmin)

class RelatedIprAdmin(admin.ModelAdmin):
    list_display = ['source', 'target', 'relationship', ]
    search_fields = ['source__name', 'target__name', 'target__document__name', ]
    raw_id_fields = ['source', 'target', ]
admin.site.register(RelatedIpr, RelatedIprAdmin)

class IprEventAdmin(admin.ModelAdmin):
    list_display = ["disclosure", "type", "by", "time"]
    list_filter = ["time", "type"]
    search_fields = ["disclosure__title", "by__name"]
    raw_id_fields = ["disclosure", "by", "msg"]
admin.site.register(IprEvent, IprEventAdmin)
