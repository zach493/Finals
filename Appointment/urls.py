from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import HomeTemplateView, AppoiTemplateView #ManageAppointmentTemplateView
from .views import register_view,user_login,logout_user, user_inbox,Successful_AppointmentView,Error_AppointmentView
from Admin.views import SATemplateView, StaffTemplateView, DashboardTemplateView, ServicesTemplateView, ResidentsTemplateView, AppointmentTemplateView, HistoryTemplateView, CrTemplateView

urlpatterns = [
    path('adm/', SATemplateView.as_view(), name="adm"),
    path('map/', AppoiTemplateView.as_view(), name='appoi'), 
    path('success_page/', Successful_AppointmentView.as_view(), name='success_page'), 
    path('error_page/', Error_AppointmentView.as_view(), name='error_page'),
    path('map/', AppoiTemplateView.as_view(), name='appoi'),    
    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
    path('staff/',StaffTemplateView.as_view(), name='staff'),
    path('services/', ServicesTemplateView.as_view(), name='services'),
    path('residents/', ResidentsTemplateView.as_view(), name='residents'),
    path('adm_appointment/', AppointmentTemplateView.as_view(), name='adm_app'),
    path('history/', HistoryTemplateView.as_view(), name='history'),
    path('cr/', CrTemplateView.as_view(), name='cr'),
    path('', HomeTemplateView.as_view(), name="home"),
    path('register/', register_view, name='register'),
    path('login/', user_login, name='login'),
    path('inbox/', user_inbox, name='inbox'),
    path(r'^logout/',logout_user,name='logout'),
    #path("manage-appointments/", ManageAppointmentTemplateView.as_view(), name="manage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
