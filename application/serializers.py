from rest_framework import serializers
from .models import Applicant, Appointment, Documents

class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class ApplicantSerializer(serializers.ModelSerializer):
    documents = DocumentsSerializer(required=False)
    appointment = AppointmentSerializer(required=False)

    class Meta:
        model = Applicant
        fields = '__all__'

    def create(self, validated_data):
        documents_data = validated_data.pop('documents', None)
        appointment_data = validated_data.pop('appointment', None)

        applicant = Applicant.objects.create(**validated_data)

        if documents_data:
            documents = Documents.objects.create(applicant=applicant, **documents_data)

        if appointment_data:
            appointment = Appointment.objects.create(**appointment_data)
            applicant.appointment = appointment
            applicant.save()

        return applicant
