from django.contrib import admin
from contacts.models import User, Person, Family
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'per_first_name', 'per_last_name')

class PersonInline(admin.TabularInline):
    model = Person

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'fam_family_name')
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