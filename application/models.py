from django.db import models
from django.contrib.auth.models import User


class Applicant(models.Model):
    family_name = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True)
    original_nationality = models.CharField(max_length=10, blank=True, null=True)
    profession = models.CharField(max_length=25, blank=True, null=True)
    religion = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    address_in_egypt = models.TextField(blank=True, null=True)
    phone_number_in_egypt = models.CharField(max_length=11, blank=True, null=True)
    port_of_arrival = models.CharField(max_length=100, blank=True, null=True)
    date_of_arrival = models.DateField(blank=True, null=True)
    requested_extension = models.CharField(max_length=50, blank=True, null=True)
    purpose_of_extension = models.TextField(blank=True, null=True)
    web_account = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='web_account', blank=True, null=True)
    branch = models.ForeignKey('Branch', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    emp = models.ForeignKey('Employee', models.DO_NOTHING, related_name='applicant_emp_set', blank=True, null=True)
    appointment = models.ForeignKey('Appointment', models.DO_NOTHING, blank=True, null=True)
    documents = models.ForeignKey('Documents', models.DO_NOTHING, blank=True, null=True)
    denied = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'applicant'


class Appointment(models.Model):
    photo = models.BinaryField(blank=True, null=True)
    fingerprints = models.BinaryField(blank=True, null=True)
    emp = models.ForeignKey('Employee', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Branch(models.Model):
    name = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'branch'


class Department(models.Model):
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documents(models.Model):
    passport_page1 = models.BinaryField(blank=True, null=True)
    passport_page2 = models.BinaryField(blank=True, null=True)
    residency_card = models.BinaryField(blank=True, null=True)
    address = models.BinaryField(blank=True, null=True)
    currency_exchange = models.BinaryField(blank=True, null=True)
    enrollment = models.BinaryField(blank=True, null=True)
    marriage_certificate = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'


class Employee(models.Model):
    dep = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)
    branch = models.ForeignKey(Branch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'
