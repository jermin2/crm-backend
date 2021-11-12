from django.contrib import admin
from contacts.models import Person, Family

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

class FamilyMembers(admin.TabularInline):
    model = Person

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'family_name')
    inlines = [
        FamilyMembers,
    ]



admin.site.register(Person, PersonAdmin)
admin.site.register(Family, FamilyAdmin)