from django.http import HttpResponse
from library_system.APIPermissions import AuthToken
from datetime import datetime, timedelta
import re
from rest_framework.views import APIView
from library_system.response import JSONResponse, ERROR_MESSAGE, SUCCESS_MESSAGE, UNAUTHORIZED, OBJECT_DOES_NOT_EXIST
from fandb.models import Student,LibraryAdmin,Session, Books, BookIssued

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
            user_id=Student.objects.create(
                student_name=name,
                student_roll_number=roll_number,
                student_email=email,
                branch=branch,
                semester=semester,
                password=password,
                year=year
            )
            user_id = str(user_id)
            user_id = re.findall(r'\d+', user_id)
            user_id = int(user_id[0])

            Session.objects.create(user_type=user_type,
                                   user_id=user_id,
                                   is_active=True
                                   )
            json = {"status": "student created"}

        elif user_type == "library_admin":
            print 'welcome'
            id = request.data["id"]
            name = request.data["name"]
            password = request.data["password"]
            user_id=LibraryAdmin.objects.create(
                admin_id=id,
                password=password,
                name=name
            )

            user_id=str(user_id)
            user_id=re.findall(r'\d+', user_id)
            user_id=int(user_id[0])

            Session.objects.create(user_type=user_type,
                                   user_id=user_id,
                                   is_active=True
            )
            json = {"status": "admin created"}

        else:
            json = {"status": "null"}


        return JSONResponse(json)

class AddBookView(APIView):

    def post(self,request):
        isbn = request.data["isbn"]
        name = request.data["name"]
        author = request.data["author"]
        domain = request.data["domain"]
        quantity = request.data["quantity"]
        Books.objects.create(
            isbn=isbn,
            name=name,
            author=author,
            domain=domain,
            quantity=quantity,
            is_issued=False,
            availibility=True
        )
        json = {"status": "Books added"}

        return JSONResponse(json)

class IssueBookView(APIView):

    def post(self,request):
        student_id = request.query_params["student_id"]
        libraryAdmin_id = request.query_params["library_admin_id"]
        book_id = request.query_params["book_id"]
        book = Books.objects.get(pk=book_id,availability=True)

        if (book):
            BookIssued.objects.create(books_id=book_id,
                                      libraryAdmin_id=libraryAdmin_id,
                                      student_id=student_id,
                                      date_of_submission=datetime.today() - timedelta(days=14),
                                      date_of_issue = datetime.today())
            book.quantity = book.quantity-1
            if (book.quantity < 1):
                book.availability = False
            book.save()
            json = {"status": "Book issued"}

            return JSONResponse(json)













