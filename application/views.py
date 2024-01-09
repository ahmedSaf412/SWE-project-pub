from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .forms import ApplicantForm, DocumentsForm
from datetime import timedelta
from django.utils import timezone
from .serializers import DocumentsSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Applicant, Appointment
from .serializers import ApplicantSerializer, AppointmentSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def applicant_with_appointment(request, applicant_id):
    try:
        applicant = Applicant.objects.get(id=applicant_id)
    except Applicant.DoesNotExist:
        return Response({'message': 'Applicant not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    elif request.method == 'POST':
        appointment_data = {'photo': request.data.get('photo'), 'fingerprints': request.data.get('fingerprints')}
        appointment_serializer = AppointmentSerializer(data=appointment_data)

        if appointment_serializer.is_valid():
            appointment = appointment_serializer.save()
            applicant.appointment = appointment
            applicant.save()
            return Response({'message': 'Images uploaded and linked to the applicant successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def review_form(request, applicant_id):
    # Check if the user is a staff member
    if not request.user.is_staff:
        return Response({'message': 'Access denied. Staff members only.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        applicant = Applicant.objects.get(id=applicant_id)
    except Applicant.DoesNotExist:
        return Response({'message': 'Applicant not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)

    if request.method == 'POST':
        decision = request.data.get('decision')

        if decision == 'accept':
            today_appointments = Applicant.objects.filter(date__date=timezone.now().date())
            start_time = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)

            if today_appointments.exists():
                latest_appointment = today_appointments.order_by('-date').first()
                next_time = latest_appointment.date + timedelta(minutes=15)
                if next_time > start_time:
                    start_time = next_time

            if start_time.hour >= 13:
                start_time = start_time + timedelta(days=1)
                start_time = start_time.replace(hour=8, minute=0, second=0, microsecond=0)

            applicant.date = start_time
            applicant.save()

            return Response({'message': 'Form accepted. Appointment scheduled successfully'}, status=status.HTTP_200_OK)

        elif decision == 'deny':
            applicant.denied = True
            applicant.save()
            return Response({'message': 'Form denied successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Invalid decision'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pending_applications(request):
    if not request.user.is_staff:
        return Response({'message': 'Access denied. Staff members only.'}, status=status.HTTP_403_FORBIDDEN)

    branch = request.query_params.get('branch')  # Get the branch from query parameters
    pending_apps = Applicant.objects.filter(date__isnull=True,denied=False, branch=branch)  # Filter by branch

    serializer = ApplicantSerializer(pending_apps, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pending_appointment(request):
    if not request.user.is_staff:
        return Response({'message': 'Access denied. Staff members only.'}, status=status.HTTP_403_FORBIDDEN)

    branch = request.query_params.get('branch')  # Get the branch from query parameters
    pending_apps = Applicant.objects.filter(appointment__isnull=True, date__isnull=False, branch=branch)  # Filter by branch

    serializer = ApplicantSerializer(pending_apps, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def submit_application(request):
    if request.method == 'POST':
        applicant_form = ApplicantForm(request.data)
        documents_serializer = DocumentsSerializer(data=request.data)

        if applicant_form.is_valid() and documents_serializer.is_valid():
            applicant = applicant_form.save(commit=False)
            documents = documents_serializer.save()

            # Assign user_id to the submitted forms (if available)
            user_id = None
            if request.user.is_authenticated:
                user_id = request.user.id
            applicant.user_id = user_id
            applicant.save()
            applicant.documents = documents
            applicant.save()

            return Response({'message': 'Application submitted successfully'}, status=200)

        return Response({'message': 'Invalid data'}, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_applications(request):
    branch = request.query_params.get('branch')  # Get the branch from query parameters

    if branch:
        applicants = Applicant.objects.filter(branch=branch)  # Filter by branch
    else:
        applicants = Applicant.objects.all()

    applicant_serializer = ApplicantSerializer(applicants, many=True)
    return Response(applicant_serializer.data)
