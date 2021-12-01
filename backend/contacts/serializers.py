from rest_framework import serializers
from .models import Person, Family, User, FamilyRole
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer, PasswordResetConfirmSerializer
from .forms import MyCustomResetPasswordForm
import datetime

class FamilyMembersSerializer(serializers.ModelSerializer):
    family_role_text = serializers.SerializerMethodField(required=False)
    per_lastName = serializers.SerializerMethodField()
    person_id = serializers.IntegerField(source='id')

    class Meta:
        model = Person
        fields = ['per_familyRole', 'per_firstName', 'per_lastName', 'id', 'person_id', 'family_role_text']

    
    def get_family_role_text(self,obj):
        if obj.per_familyRole:
            return obj.per_familyRole.family_role
        else :
            return "Not set"

    def get_per_lastName(self, obj):
        if obj.per_lastName:
            return obj.per_lastName
        else :
            return obj.family.fam_familyName

    def to_internal_value(self, data):
        if 'family' in data:
            data.pop('family')
        person_id = data.pop('person_id')
        if int(person_id) < 0:
            person_id = None
        serializer = PersonSerializer(data=data)
        serializer.is_valid()
        person_data = serializer.validated_data
        obj, created = Person.objects.update_or_create( id=person_id, defaults={**person_data})
        return obj

class FamilySerializer(serializers.ModelSerializer):
    family_members = FamilyMembersSerializer( many=True, required=True)
    family_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = Family
        fields = ['fam_familyName','id', 'family_id',  'fam_familyEmail', 'fam_familyAddress', 'family_members']

    def update(self, instance, validated_data):
        print("update", validated_data)
        family_members = validated_data.pop('family_members')
        for person in family_members:
            # Assume we have people object by this stage
            person.family = instance
            person.save()

        Family.objects.filter(id=instance.id).update(**validated_data)
        return instance

class LastNameField(serializers.Field):
    def to_representation(self, obj):
        if obj.per_lastName == "":
            return obj.family.fam_familyName
        return obj.per_lastName
    def to_internal_value(self, data):
        return {'per_lastName': data}

class BirthdayField(serializers.Field):
    def to_representation(self, obj):
        if obj.per_birthday == None:
            return ""
        return obj.per_birthday
    def to_internal_value(self, data):
        if data == "":
            return {'per_birthday': None}
        return {'per_birthday': data}

class PersonFamilySerializer(FamilySerializer):
    family_members = FamilyMembersSerializer( many=True, required=False, read_only=True)
    action = serializers.CharField(max_length=10, required=False)
    family_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Family
        fields = ['fam_familyName','id', 'family_id',  'fam_familyEmail', 'fam_familyAddress', 'family_members', 'action']

    def to_internal_value(self, data):
        # print("to internval family: ", data)
        action = data.pop('action')

        if action == 'fetch':
            return Family.objects.get(id=data['id'])
        try:
            
            if action == 'create': 
            # Create new family
                family_data = super(PersonFamilySerializer, self).to_internal_value(data['new'])
                return Family.objects.create(**family_data)
            if action == 'update':
                obj_id = data['id']
                family_data = super(PersonFamilySerializer, self).to_internal_value(data)
                Family.objects.filter(id=obj_id).update(**family_data)
                # print("family_data: ", family_data)
                return Family.objects.get(id=obj_id)

        except KeyError:
            raise serializers.ValidationError(
                'id is a required field.'
            )
        except ValueError:
            raise serializers.ValidationError(
                'id must be an integer.'
            )


class PersonSerializer(serializers.ModelSerializer):
    school_year = serializers.SerializerMethodField(required=False)
    per_birthday = BirthdayField(source='*', allow_null=True)
    per_lastName = LastNameField(source='*')
    age_group = serializers.SerializerMethodField()
    family = PersonFamilySerializer(required=False)

    class Meta:
        model = Person
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert school year to per_yearOneYear
        if data.get('school_year') == None or data.get('school_year') == "":
            data['school_year'] = None
        else:
            data['per_yearOneYear'] = self.reverseSchoolYear( int(data.get('school_year')) )

        if data.get('per_birthday') == None or data.get('per_birthday') == "":
            data['per_birthday'] = None

        return super(PersonSerializer, self).to_internal_value(data)

    def reverseSchoolYear(self, schoolYear):
        if schoolYear > 1000:
            return schoolYear - 13
        else:
            return datetime.datetime.now().year - schoolYear
        
    def update(self, instance, validated_data):
        Person.objects.filter(id=instance.id).update(**validated_data)
        return instance

    def create(self, validated_data):
        person = Person.objects.create(**validated_data)
        return person

    def get_school_year(self, obj):
        if obj.per_yearOneYear:
            school_year = datetime.datetime.now().year - obj.per_yearOneYear
            if school_year < 13 :
                return (datetime.datetime.now().year - obj.per_yearOneYear)
            else:
                return obj.per_yearOneYear + 13
        return ''

    def get_age_group(self, obj):
        if obj.per_yearOneYear:
            return "To Be Implemented"
        return "Please set school / graduation year"

class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = ['id','email', 'role', 'user_permissions', 'person']

class PasswordResetSerializer(_PasswordResetSerializer):
    def validate_email(self, value):
        # I override this line so that I can use MyCustomResetPasswordForm
        self.reset_form = MyCustomResetPasswordForm(data=self.initial_data)  
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

class FamilyRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = FamilyRole
        fields = '__all__'