from django.db import models

# Create your models here.
BED_TYPE = [(0, 'General'), (1, 'Semi-Private'), (2, 'Private')]


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "{} , {}".format(self.name, self.patient_id)


class Bed(models.Model):
    bed_number = models.AutoField(primary_key=True)
    availability = models.BooleanField(default=True)
    bed_type_id = models.IntegerField(choices=BED_TYPE)
    # patient = models.OneToOneField(Patient, blank=True, default=None, null=True, on_delete=models.PROTECT)

    def __str__(self):
        bed_type = list(filter(lambda x: x[0] == self.bed_type_id, BED_TYPE))[0][1]
        return "bed_number {} and bed type {}".format(self.bed_number, bed_type)


    @classmethod
    def get_all_bed(cls, status):
        bed = Bed.objects.filter(availability=status).all()
        return bed
    #
    def get_bed_type(self):
        bed_type = list(filter(lambda x: x[0] == self.bed_type_id, BED_TYPE))[0][1]
        return bed_type
    #
    # def get_patient_name(self):
    #     if self.patient_id:
    #         patient = Patient.objects.filter(patient_id=self.patient_id).get()
    #         return patient.name
    #
    #     return None


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, db_column='bed_number')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    checkout = models.DateTimeField(default=None, null=True)

    @classmethod
    def check_in(cls, patient_id, bed_type_id):
        bed = Bed.objects.filter(bed_type_id= bed_type_id,availability=True)
        if bed:
            bed = bed.first()
            bed_number = bed.bed_number
            transaction = Transaction(patient_id=patient_id, bed_id=bed_number)
            transaction.save()
            bed.availability = False
            bed.save()
            return True
        else:
            return False

    def __str__(self):
        return "Transaction Id : {} , Bed number : {} ,Patient{}".format(self.transaction_id, self.bed_id,
                                    self.patient_id)