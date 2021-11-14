from rest_framework import serializers
from .models import Person, Family, User
from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from django.contrib.auth.forms import PasswordResetForm
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.urls import reverse
from allauth.account.utils import (filter_users_by_email,
                                    user_pk_to_url_str, user_username)
from .forms import MyCustomResetPasswordForm

from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
default_token_generator = EmailAwarePasswordResetTokenGenerator()



class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer()

    class Meta:
        model = Person
        fields = '__all__'

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
