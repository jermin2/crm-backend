from django.contrib import admin
from contacts.models import User, Person, Family, FamilyRole, Tag
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'per_firstName', 'per_lastName')

class PersonInline(admin.TabularInline):
    model = Person

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fam_familyName')
    inlines = [
        PersonInline,
    ]

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    inlines = [PersonInline]
    exclude = ('first_name', 'last_name')

admin.site.register(Person, PersonAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(FamilyRole)
admin.site.register(Tag)