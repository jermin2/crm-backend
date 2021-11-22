from django.shortcuts import render
from .serializers import PersonSerializer, FamilySerializer
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from .models import Person, Family

from dj_rest_auth.registration.views import ConfirmEmailView

from allauth.account.signals import email_confirmed
from django.dispatch import receiver

class FamilyView(viewsets.ModelViewSet):
    serializer_class = FamilySerializer
    queryset = Family.objects.all()

# Create your views here.
class PersonView(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Person.objects.all()

    def create(self, request):
        # person = Person.objects.create(name="John")
        print(request.data.get('per_first_name'))
        info = dict()
        info['per_first_name'] = request.data.get('per_first_name')
        info['per_last_name'] = request.data.get('per_last_name')
        info['per_email'] = request.data.get('per_email')
        info['per_day_of_birth'] = request.data.get('per_day_of_birth')
        info['per_month_of_birth'] = request.data.get('per_month_of_birth')
        info['per_year_of_birth'] = request.data.get('per_year_of_birth')
        family_state = request.data.get('familyState')

        request_cpy = dict(request.data)
        #request_cpy.pop('csrfmiddlewaretoken')


        # user = request_cpy.pop('user')
        print(info)

        try:
            person = Person(
                **info
            )
            print(person.per_first_name, person.per_last_name)
            # person.save()
            return JsonResponse({"success": "POST request required."}, status=200)

        except Exception as e:
            print(e)
            return JsonResponse({"error": "POST request required."}, status=400)

        return JsonResponse({"success": "POST request required."}, status=200)
        pass


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.role = 'user'
    print("email confirmed")
    user.save()



class CustomConfirmEmailView(ConfirmEmailView):
   pass