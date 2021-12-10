"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# from rest_framework import routers
from contacts import views
from contacts import routers
from dj_rest_auth.registration.views import VerifyEmailView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from django.conf import settings
from django.conf.urls.static import static




router = routers.DefaultRouter()
router.register('contact', views.PersonView)
router.register('family', views.FamilyView)
router.register('familyRole', views.FamilyRoleView)
router.register('avatar', views.AvatarView)
router.register('user', views.UserView)
router.register('tag', views.TagView, 'tag-detail')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/contacts-app/ContactsTags/', views.contacts_tag, name='contacts_tag'),
    path('api/contacts-app/updatetags/<id>', views.update_person_tags, name='update_person_tags'),
    path('api/contacts-app/updatefamilytags/<id>', views.update_family_tags, name='update_family_tags'),
    path('api/contacts-app/', include(router.urls)),
    path(
        'api/auth/password/reset/confirm/<slug:uidb64>/<slug:token>/',
        PasswordResetConfirmView.as_view()
    ),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/account-confirm-email/<str:key>/', views.CustomConfirmEmailView.as_view()),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/registration/account-confirm-email', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('api/contacts-app/user/', views.get_user, name='user'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)