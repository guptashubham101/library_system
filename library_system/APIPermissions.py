from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from fandb.models import Session, Student, LibraryAdmin


class AuthToken(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def check_token(self, request, headers):
        print 'sop'
        if 'HTTP_SESSIONID' in headers:
            print 'pos'
            last_month = datetime.today() - timedelta(days=100)
            print last_month

            session = Session.objects.filter(session_id=headers['HTTP_SESSIONID'],
                                             created_on__gte=last_month, is_active=True).first()
            print session
            if session:
                print 'enter'
                if session.user_type == 'library_admin':
                    print '1'
                    request.user = LibraryAdmin.objects.get(pk=session.user_id)
                elif session.user_type == 'student':
                    print '2'
                    request.user = Student.objects.get(pk=session.user_id)
                else:
                    print 'No such user exists'
                return request.user
            else:
                return False
        else:
            return False

    def has_permission(self, request, view):
        return self.check_token(request, request.META)
