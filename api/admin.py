from api.models import OsTemplate, OsTemplate2, Os, install
from django.contrib import admin

class OsTemplateAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Distro Info:', {'fields': ['Tos', 'Tid', 'Tinstall']}),
        ('Display Info:', {'fields': ['Tname', 'Ttitle', 'Ttext', 'Tlink']}),
    ]
    list_display = ('Tos', 'Tid', 'Tinstall', 'Ttitle')
    search_fields = ['Tos', 'Tid', 'Tinstall', 'Tname']

class OsAdmin(admin.ModelAdmin):
	list_display = ('id','os', 'name')

class installAdmin(admin.ModelAdmin):
	list_display = ('id','type')

admin.site.register(Os, OsAdmin)
admin.site.register(install, installAdmin)
admin.site.register(OsTemplate, OsTemplateAdmin)
admin.site.register(OsTemplate2, OsTemplateAdmin)
