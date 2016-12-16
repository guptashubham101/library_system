from django.http import HttpResponse
from library_system.APIPermissions import AuthToken
from datetime import datetime, timedelta
import re
from rest_framework.views import APIView
from library_system.response import JSONResponse, ERROR_MESSAGE, SUCCESS_MESSAGE, UNAUTHORIZED, OBJECT_DOES_NOT_EXIST
from fandb.models import Student,LibraryAdmin,Session, Books, BookIssued,Fine
from fandb.serializers import StudentSerializer,BookDetailsSerializer, LoginDetailsLibrarySerializer,LoginDetailsStudentSerializer
from hash import get_hexdigest
import random
from library_system.sendgrid_mail import send_mail

class RegistrationView(APIView):

    def post(self, request):
        print 'sop'
        user_type = request.data['user_type']

        print user_type
        if user_type == 'student':
            name = request.data['name']
            roll_number = request.data['roll_number']
            email = request.data['email']
            branch = request.data['branch']
            semester = request.data['semester']
            year = request.data['year']

            student = Student.objects.filter(student_roll_number=roll_number)

            if(student):
                json = {"result": False}

            else:
                Student.objects.create(
                    student_name=name,
                    student_roll_number=roll_number,
                    student_email=email,
                    branch=branch,
                    semester=semester,
                    password='123456',
                    year=year
                )

                json = {"result": True}

        elif user_type == "library_admin":
            password = request.data['password']
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            print 'po'
            hsh = get_hexdigest(algo, salt, password)
            password = '%s$%s$%s' % (algo, salt, hsh)
            print 'welcome'
            id = request.data["email"]
            name = request.data["name"]
            print id
            print name
            admin = LibraryAdmin.objects.filter(admin_id=id)
            print admin

            if(admin):
                json = {"result": False}

            else:

                LibraryAdmin.objects.create(
                    admin_id=id,
                    password=password,
                    name=name
                )

                json = {"result": True}

        else:
            json = {"result": False}


        return JSONResponse(json)


class LoginView(APIView):
    def post(self, request):
        print 'login'
        user_id = request.data["email"]
        password = request.data["password"]
        student = LibraryAdmin.objects.get(admin_id=user_id)
        print student

        print 'skip'
        enc_password = student.password
        algo, salt, hsh = enc_password.split('$')
        print algo
        print salt
        print hsh
        print enc_password
        if hsh == get_hexdigest(algo, salt, password):

            session = Session.objects.create(user_id=student.id,
                                   is_active=True
                                   )
            print session

            response_data = {"sessionId": session.session_id, "result": True,
                             "user": {
                                 "name": student.name,
                                 "email": student.admin_id,
                                 "id": student.id
                             }}
            return JSONResponse(response_data)
        else:
            json = {"result": False}
            return JSONResponse(json)

class LogoutView(APIView):
    def put(self, request):
        user_id = request.data["user_id"]
        session = Session.objects.filter(user_id=user_id,is_active=True)
        json = {"status": "You are already logged out"}
        for s in session:
            s.is_active=False
            s.save()
            json = {"status": "You are successfully logged out"}

        return JSONResponse(json)



class AddBookView(APIView):

    def post(self,request):
        print 'hello'
        isbn = request.data["isbn"]
        name = request.data["name"]
        author = request.data["author"]
        domain = request.data["domain"]
        quantity = request.data["quantity"]
        print quantity
        if quantity > 0:
            print quantity
            is_avail = True
        else:
            print quantity
            is_avail = False

        Books.objects.create(
            ISBN=isbn,
            name=name,
            author=author,
            domain=domain,
            quantity=quantity,
            is_issued=False,
            availability=is_avail
        )
        json = {"result": True}

        return JSONResponse(json)

class IssueBookView(APIView):
    permission_classes = (AuthToken,)

    def post(self,request):
        print 'welcome'
        print request.query_params
        roll_number = request.query_params["roll_number"]
        print roll_number

        student = Student.objects.get(student_roll_number=roll_number)



        library_admin_id = request.query_params["admin_id"]

        isbn = request.query_params["isbn"]
        print isbn

        book = Books.objects.get(ISBN=isbn)
        print book

        library = LibraryAdmin.objects.get(admin_id=library_admin_id)
        print library

        print 'hello'
        if book.availability is True:


            print 'sss'
            BookIssued.objects.create(books_id=book.id,
                                      library_admin_id=library.id,
                                      student_id=student.id,
                                      date_of_submission=datetime.today() + timedelta(days=14),
                                      date_of_issue = datetime.today())
            book.quantity = book.quantity-1
            if (book.quantity < 1):
                book.availability = False
            book.save()
            json = {"message": "Book issued","result": True}
        else:
            json = {"message" : "Book out of stock","result": False}

        return JSONResponse(json)

class StudentListView(APIView):

    def get(self,request):

        roll_number = request.query_params["roll_number"]

        student_id = Student.objects.get(student_roll_number=roll_number)

        books = BookIssued.objects.filter(student_id=student_id.id, date_of_submission__lt=datetime.today())

        for book in books:
            print 'fine'
            days = datetime.today() - book.date_of_submission.replace(tzinfo=None)
            days = str(days)
            idx = days.find('days')
            days = days[:idx]
            days = int(days)
            amount = days * 10

            fine = Fine.objects.filter(student=student_id.id,books_id=book.books_id)

            if(fine):
                pass

            else:

                Fine.objects.create(student_id=student_id.id,
                                    is_paid=False,
                                    books_id=book.books_id,
                                    days=days,
                                    amount=amount)

        response_data = {}

        response_data['data'] = StudentSerializer(
            instance=Student.objects.get(pk=student_id.id)).data

        response_data['result'] = True

        return JSONResponse(response_data)


class BookListView(APIView):

    def get(self,request):
        print 'hello'
        print request.query_params
        print request.query_params["isbn"]
        isbn = request.query_params["isbn"]

        book_id = Books.objects.get(ISBN=isbn)
        print book_id
        print book_id.id

        books = BookIssued.objects.filter(books_id=book_id.id, date_of_submission__lt=datetime.today())

        for book in books:
            print 'fine'
            days = datetime.today() - book.date_of_submission.replace(tzinfo=None)
            days = str(days)
            idx = days.find('days')
            days = days[:idx]
            days = int(days)
            amount = days * 10

            fine = Fine.objects.filter(student=book.student_id, books_id=book_id.id)

            if (fine):
                pass

            else:

                Fine.objects.create(student_id=book.student_id,
                                    is_paid=False,
                                    books_id=book_id.id,
                                    days=days,
                                    amount=amount)

        response_data = {}
        response_data['data'] = BookDetailsSerializer(
            instance=Books.objects.get(pk=book_id.id)).data

        response_data['result'] = True

        return JSONResponse(response_data)


class FeesPaidView(APIView):

    def put(self,request):
        print 'hello'
        print request.query_params
        roll_number = request.query_params["roll_number"]
        print roll_number

        student = Student.objects.get(student_roll_number=roll_number)

        isbn = request.query_params["isbn"]
        print isbn

        book = Books.objects.get(ISBN=isbn)
        print book

        fine=Fine.objects.get(student_id=student.id,books_id=book.id)
        json = {"status": "Fine already paid"}
        if fine.is_paid is False:
            fine.is_paid=True
            fine.save()
            json = {"result": True}

        return JSONResponse(json)

class SendMailView(APIView):
    def post(self,request):

        send_mail()
        json = {"status": "Mail sent"}
        return JSONResponse(json)






















