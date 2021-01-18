from django.contrib import admin
from bedmanagement.models import Patient, Bed, Transaction
# Register your models here.

class PatientView(admin.ModelAdmin):
    list_display = ['patient_id', 'name', 'email', 'phone']

class BedView(admin.ModelAdmin):
    list_display = ['bed_type_id', 'bed_number', 'availability']


class TransactionView(admin.ModelAdmin):
    list_display = ['patient_name', 'transaction_id', 'checkout']
    
    def patient_name(self, obj):
        return obj.patient.name

admin.site.register(Patient, PatientView)
admin.site.register(Bed, BedView)
admin.site.register(Transaction, TransactionView)

