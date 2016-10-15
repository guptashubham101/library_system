from django.http import HttpResponse
from library_system.APIPermissions import AuthToken
from datetime import datetime, timedelta
import re
from rest_framework.views import APIView
from library_system.response import JSONResponse, ERROR_MESSAGE, SUCCESS_MESSAGE, UNAUTHORIZED, OBJECT_DOES_NOT_EXIST
from fandb.models import Student,LibraryAdmin,Session, Books, BookIssued,Fine
from fandb.serializers import StudentSerializer,BookDetailsSerializer, LoginDetailsSerializer

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
            password = request.data['password']
            semester = request.data['semester']
            year = request.data['year']
            Student.objects.create(
                student_name=name,
                student_roll_number=roll_number,
                student_email=email,
                branch=branch,
                semester=semester,
                password=password,
                year=year
            )

            json = {"status": "student created"}

        elif user_type == "library_admin":
            print 'welcome'
            id = request.data["id"]
            name = request.data["name"]
            password = request.data["password"]
            LibraryAdmin.objects.create(
                admin_id=id,
                password=password,
                name=name
            )

            json = {"status": "admin created"}

        else:
            json = {"status": "null"}


        return JSONResponse(json)


class LoginView(APIView):
    def post(self, request):
        user_id = request.data["user_id"]
        user_type = request.data["user_type"]

        Session.objects.create(user_type=user_type,
                               user_id=user_id,
                               is_active=True
                               )

        response_data = LoginDetailsSerializer(instance=LibraryAdmin.objects.filter(pk=user_id),
                                               many=True).data
        return JSONResponse(response_data)

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
        json = {"status": "Books added"}

        return JSONResponse(json)

class IssueBookView(APIView):
    permission_classes = (AuthToken,)

    def post(self,request):
        student_id = request.query_params["student_id"]

        library_admin_id = request.query_params["library_admin_id"]

        book_id = request.query_params["book_id"]
        book = Books.objects.get(pk=book_id)
        if book.availability is True:



            BookIssued.objects.create(books_id=book_id,
                                      library_admin_id=library_admin_id,
                                      student_id=student_id,
                                      date_of_submission=datetime.today() + timedelta(days=14),
                                      date_of_issue = datetime.today())
            book.quantity = book.quantity-1
            if (book.quantity < 1):
                book.availability = False
            book.save()
            json = {"status": "Book issued"}
        else:
            json = {"status" : "Book out of stock"}

        return JSONResponse(json)

class StudentListView(APIView):

    def get(self,request):

        student_id = request.query_params["student_id"]

        response_data = StudentSerializer(
            instance=Student.objects.filter(pk=student_id),many=True).data

        return JSONResponse(response_data)


class BookListView(APIView):

    def get(self,request):
        book_id = request.query_params["book_id"]

        response_data = BookDetailsSerializer(
            instance=Books.objects.filter(pk=book_id),many=True).data

        return JSONResponse(response_data)

class LateSubmissionView(APIView):

    def post(self,request):

        student_id = request.data["student_id"]
        books = BookIssued.objects.filter(student_id=student_id,date_of_submission__lt=datetime.today())

        for book in books:
            days = datetime.today()-book.date_of_submission.replace(tzinfo=None)
            days=str(days)
            idx = days.find('days')
            days = days[:idx]
            days = int(days)
            amount = days*10

            Fine.objects.create(student_id=student_id,
                                is_paid=False,
                                books_id=book.books_id,
                                days=days,
                                amount=amount)

        json = {"status": "Fine added"}

        return JSONResponse(json)

class FeesPaidView(APIView):

    def put(self,request):
        student_id = request.query_params["student_id"]
        books_id = request.query_params["books_id"]
        fine=Fine.objects.get(student_id=student_id,books_id=books_id)
        json = {"status": "Fine already paid"}
        if fine.is_paid is False:
            fine.is_paid=True
            fine.save()
            json = {"status": "Fine paid"}

        return JSONResponse(json)
























