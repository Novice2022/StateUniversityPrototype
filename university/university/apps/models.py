# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
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


class Department(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    institute = models.ForeignKey('Institute', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class Groupofstudents(models.Model):
    id = models.SmallAutoField(primary_key=True)
    number = models.IntegerField()
    department = models.ForeignKey(Department, models.DO_NOTHING, blank=True, null=True)
    educational_course = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groupofstudents'


class Institute(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'institute'


class Schedule(models.Model):
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Groupofstudents, models.DO_NOTHING, blank=True, null=True)
    couple_number = models.IntegerField()
    week_day = models.CharField(max_length=11)
    calendar_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule'


class Scores(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey('Student', models.DO_NOTHING, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING, blank=True, null=True)
    issued_date = models.DateTimeField(blank=True, null=True)
    scores_amount = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'scores'


class Student(models.Model):
    group_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'student'


class Subject(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    lesson_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'subject'


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'teacher'
