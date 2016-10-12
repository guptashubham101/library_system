from django.conf.urls import url

from fandb.views import RegistrationView, AddBookView, IssueBookView

urlpatterns = [
    url(r'registration', RegistrationView.as_view()),
    url(r'add/book', AddBookView.as_view()),
    url(r'issue/book', IssueBookView.as_view())
    ]