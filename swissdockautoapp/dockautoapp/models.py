# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class Estadojob(models.Model):
    idestado = models.AutoField(db_column='IDESTADO', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estadojob'


class Job(models.Model):
    idjob = models.AutoField(db_column='IDJOB', primary_key=True)  # Field name made lowercase.
    idproyecto = models.ForeignKey('Proyectojob', models.DO_NOTHING, db_column='IDPROYECTO', blank=True, null=True)  # Field name made lowercase.
    idestado = models.ForeignKey(Estadojob, models.DO_NOTHING, db_column='IDESTADO', blank=True, null=True)  # Field name made lowercase.
    idtarget = models.ForeignKey('Target', models.DO_NOTHING, db_column='IDTARGET', blank=True, null=True)  # Field name made lowercase.
    idligand = models.ForeignKey('Ligand', models.DO_NOTHING, db_column='IDLIGAND', blank=True, null=True)  # Field name made lowercase.
    swissdockid = models.CharField(db_column='SWISSDOCKID', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pathresultado = models.TextField(db_column='PATHRESULTADO', blank=True, null=True)  # Field name made lowercase.
    errorresultado = models.FloatField(db_column='ERRORRESULTADO', blank=True, null=True)  # Field name made lowercase.
    deltagpromedio = models.FloatField(db_column='DELTAGPROMEDIO', blank=True, null=True)  # Field name made lowercase.
    fechahoracreacion = models.DateTimeField(db_column='FECHAHORACREACION', blank=True, null=True)  # Field name made lowercase.
    fechahoratermino = models.DateTimeField(db_column='FECHAHORATERMINO', blank=True, null=True)  # Field name made lowercase.
    nombrejob = models.TextField(db_column='NOMBREJOB', blank=True, null=True)  # Field name made lowercase.
    puntosentrada = models.TextField(db_column='PUNTOSENTRADA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'job'


class Ligand(models.Model):
    idligand = models.AutoField(db_column='IDLIGAND', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ligand'


class Proyectojob(models.Model):
    idproyecto = models.AutoField(db_column='IDPROYECTO', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    fechahoracreacion = models.DateTimeField(db_column='FECHAHORACREACION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proyectojob'


class Puntodocking(models.Model):
    idpuntodocking = models.AutoField(db_column='IDPUNTODOCKING', primary_key=True)  # Field name made lowercase.
    idjob = models.ForeignKey(Job, models.DO_NOTHING, db_column='IDJOB', blank=True, null=True)  # Field name made lowercase.
    xpunto = models.FloatField(db_column='XPUNTO', blank=True, null=True)  # Field name made lowercase.
    ypunto = models.FloatField(db_column='YPUNTO', blank=True, null=True)  # Field name made lowercase.
    zpunto = models.FloatField(db_column='ZPUNTO', blank=True, null=True)  # Field name made lowercase.
    numberpunto = models.IntegerField(db_column='NUMBERPUNTO', blank=True, null=True)  # Field name made lowercase.
    charpunto = models.CharField(db_column='CHARPUNTO', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'puntodocking'


class Target(models.Model):
    idtarget = models.AutoField(db_column='IDTARGET', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=200, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'target'
