from django.contrib import admin
from django.urls import path, include
from Admin.views import SATemplateView


urlpatterns = [
    path("", include("Admin.urls")),
    path("", include("Appointment.urls")),  # Remove the 'namespace' parameter
    path("", admin.site.urls),
]
