from django.contrib import admin
from facts.models import PhoneNumber, CatFact


def make_approved(modeladmin, request, queryset):
    queryset.update(approved=True)

make_approved.short_description = "Mark Fact as Approved"

class CatFactAdmin(admin.ModelAdmin):
    fields = ('fact', 'approved')
    list_display = ('fact', 'approved')
    actions = [make_approved]

admin.site.register(PhoneNumber)
admin.site.register(CatFact, CatFactAdmin)
