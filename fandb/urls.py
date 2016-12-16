from django.conf.urls import url

from fandb.views import RegistrationView, AddBookView, IssueBookView,BookListView,StudentListView,LoginView,LogoutView,FeesPaidView,SendMailView

urlpatterns = [
    url(r'registration', RegistrationView.as_view()),
    url(r'add/book', AddBookView.as_view()),
    url(r'issue/book', IssueBookView.as_view()),
    url(r'list/books', BookListView.as_view()),
    url(r'list/student/details', StudentListView.as_view()),
    url(r'login/',LoginView.as_view()),
    url(r'logout',LogoutView.as_view()),
    url(r'fees/paid',FeesPaidView.as_view()),
    url(r'send/mail',SendMailView.as_view())

    ]