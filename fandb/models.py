from django.conf import settings
import uuid
from django.db import models


class  BookIssued(models.Model):
    student = models.ForeignKey('Student')
    library_admin = models.ForeignKey('LibraryAdmin')
    books = models.ForeignKey('Books')
    date_of_submission = models.DateTimeField()
    date_of_issue = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book_issued'


class Books(models.Model):

    ISBN = models.IntegerField()
    availability = models.BooleanField(default=False)

    is_issued = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

    class Meta:
        db_table = 'books'


class Fine(models.Model):
    student = models.ForeignKey('Student')
    is_paid = models.BooleanField(default=False)
    days = models.IntegerField()

    class Meta:
        db_table = 'fine'


class LibraryAdmin(models.Model):
    admin_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'library_admin'

    def __str__(self):
        return "%s" % (self.id)


class Session(models.Model):
    session_id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField()
    user_id = models.IntegerField()
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'session'


class Student(models.Model):
    student_name = models.CharField(max_length=255)
    student_roll_number = models.CharField(max_length=255)
    student_email = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    semester = models.IntegerField()
    year = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return "%s" % (self.id)


















