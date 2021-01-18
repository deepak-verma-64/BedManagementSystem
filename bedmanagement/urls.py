from django.urls import path
from bedmanagement.views import AssignPatient,\
    BedStatusView, PatientCheckoutView, PatientView, BedDetailView

urlpatterns = [
    path('bed/assign', AssignPatient.as_view()),
    path('bed/status', BedStatusView.as_view()),
    path('patient/checkout', PatientCheckoutView.as_view()),
    path('patient/', PatientView.as_view()),
    path('bed/availability/', BedDetailView.as_view())


]
