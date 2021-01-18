from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from bedmanagement.models import Patient, Bed, Transaction
from django.core import serializers
# Create your views here.
import json
from datetime import datetime
from bedmanagement.models import BED_TYPE


class AssignPatient(View):

    def post(self, request):
        ''' If any patient comes and asks for a specific bed: assign them particular bed if bed
        available else: show the message &quot;not available as of now
        '''

        request_data = json.loads(request.body.decode('utf-8'))
        try:
            patient_id = int(request_data.get('patient_id'))
            bed_type_id = int(request_data.get('bed_type_id'))
        except ValueError:
            return JsonResponse({'msg': 'Patient, Type both should be Integer'}, status=400)

        bed = Bed.objects.filter(availability=True, bed_type_id=bed_type_id)
        if bed:
            patient = Patient.objects.filter(patient_id=patient_id)
            if patient:
                check_in = Transaction.check_in(patient_id, bed_type_id)
                if check_in:
                    return JsonResponse({"msg": "Success Assign bed to patient"}, status=200)
                else:
                    return JsonResponse({"msg": "No bed available for given bed type{}".format(bed_type_id)},
                                        status=200)
            else:
                return JsonResponse({"msg": "Patient is not present"}, status=400)
        else:
            return JsonResponse({"msg": "Bed not available as of now"}, status=400)


class BedStatusView(View):
    def get(self, request):
        '''Status of bed:input- bed_number
            output- patient_name, bed_type'''

        get_data = request.GET
        bed_number = get_data.get('bed_number')

        bed = Bed.objects.filter(bed_number=bed_number)
        if bed:
            bed = bed.get()
            transaction = Transaction.objects.filter(bed_id=bed_number, checkout=None)
            if transaction:
                transaction = transaction.get()
                patient_name = transaction.patient.name
                bed_type_name = transaction.bed.get_bed_type()

                return JsonResponse({"data": {"patient_name": patient_name, "bed_type_name": bed_type_name}},
                                    status=200)
            else:
                return JsonResponse({"msg": "Could not found patient"},
                                    status=200)
        else:
            return JsonResponse({"msg": "Bed Number Not Found"}, status=400)


class PatientCheckoutView(View):
    def post(self, request):
        '''Patient Checkout:
            customer leave the bed so the bed is again free for use
        '''
        post_data = json.loads(request.body.decode('utf-8'))
        patient_id = post_data.get('patient_id')

        transaction = Transaction.objects.filter(patient_id=patient_id)
        if transaction:
            transaction = transaction.get()
            bed_number = transaction.bed_id
            bed = Bed.objects.filter(bed_number=bed_number)
            if bed:
                bed = bed.get()
                bed.availability = True
                bed.save()
                transaction.checkout = datetime.now()
                transaction.save()

                return JsonResponse({"msg": "Patient Checkout Successfully"}, status=200)

        else:
            return JsonResponse({"msg": "Patient id not found"}, status=400)


class PatientView(View):

    def get_all_patient(self, request):
        all_patient = serializers.serialize("json", Patient.objects.all())
        return HttpResponse(all_patient)

    def get(self, request):
        '''Get the name of all patients which opt for a specific type of bed'''

        get_data = request.GET
        if not get_data:
            return self.get_all_patient(request)

        try:
            bed_type_id = int(get_data.get('bed_type_id'))
        except ValueError:
            return JsonResponse({"msg": "Type Should be Integer"}, status=400)

        bed_numbers = Bed.objects.filter(bed_type_id=bed_type_id).values("bed_number")
        transactions = Transaction.objects.filter(bed_id__in=bed_numbers)

        data = [{transaction.patient.patient_id: transaction.patient.name} for transaction in transactions]

        return JsonResponse({"data": data})


class BedDetailView(View):

    def get(self, request):
        ''' 1 status of types of beds: empty or full
        2 list of beds which are free/occupy
        '''
        get_data = request.GET
        bed_type_id = get_data.get('bed_type_id')
        available = get_data.get('status')

        if bed_type_id:
            bed = Bed.objects.filter(bed_type_id=bed_type_id, availability=True)
            if bed:
                return JsonResponse({"msg": 'Bed Available'})
            else:
                return JsonResponse({"msg": 'Bed Full'})
        else:
            beds = Bed.get_all_bed(available)
            if beds:
                data = []
                for bed in beds:
                    data.append({"bed_number": bed.bed_number, "bed_type": bed.get_bed_type()})
                return JsonResponse({"data": data})
            else:
                return JsonResponse({"msg": "No bed available with {}".format(str(available))})
