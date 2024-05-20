from django.urls import path
from Admin.views import delete_resident,delete_staff,delete_service,move_to_finished
from Admin.views import SATemplateView, StaffTemplateView, DashboardTemplateView,GuardianTemplateView, ServicesTemplateView, ResidentsTemplateView, AppointmentTemplateView, HistoryTemplateView, CrTemplateView
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adm/', SATemplateView.as_view(), name="adm"),
    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
    path('staff/', StaffTemplateView.as_view(), name='staff'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('services/', ServicesTemplateView.as_view(), name='services'),
    #path('delete_service/', delete_service, name='delete_service'),
    path('delete_service/<int:service_id>/', views.delete_service, name='delete_service'),
    path('edit_service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('add_service/', views.add_service, name='add_service'),
    path('residents/', ResidentsTemplateView.as_view(), name='residents'),
    path('delete_resident/<int:resident_id>/', delete_resident, name='delete_resident'),
    path('adm_appointment/', AppointmentTemplateView.as_view(), name='adm_app'),
    path('guardian_appointment/', GuardianTemplateView.as_view(), name='guardian_app'),
    path('accept_appointment/', views.accept_appointment, name='accept_appointment'),
    path('reject_appointment/', views.reject_appointment, name='reject_appointment'),
    path('finished_appointment/', views.move_to_finished, name='finished_appointment'),
    path('move_to_finished/', move_to_finished, name='move_to_finished'),
    path('history/', HistoryTemplateView.as_view(), name='history'),
    path('cr/', CrTemplateView.as_view(), name='cr'),
    path('logout/', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urls.py is used to define URL patterns that route HTTP requests to the appropriate view functions or class-based views.