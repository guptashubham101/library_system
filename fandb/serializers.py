from rest_framework import serializers

from fandb.models import Student,BookIssued,Books,LibraryAdmin,Fine

class FineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fine
        fields = ('is_paid','days','amount')

class StudentListSerializer(serializers.ModelSerializer):

    fine = serializers.SerializerMethodField(source='get_fine')
    print 'ssss'
    class Meta:
        model = Student
        fields = ('student_name', 'student_roll_number', 'student_email', 'branch','semester','year','fine')

    def get_fine(self, obj):
        return FineSerializer(instance=Fine.objects.filter(student_id=obj.id, books_id=self.context.get('c')),
                              many=True).data

class BookSerializer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField(source='get_student')

    class Meta:
        model = BookIssued
        fields = ('student','date_of_submission','date_of_issue')

    def get_student(self, obj):
        return StudentListSerializer(instance=Student.objects.get(pk=obj.student_id),
                                  context={'c': self.context.get('first_model_id')}).data


class BookDetailsSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField(source='get_details')
    class Meta:
        model=Books

        include = ('details',)

    def get_details(self, obj):

        return BookSerializer(instance=BookIssued.objects.filter(books_id=obj.id),
                                    many=True,context={'first_model_id': obj.id}).data

class BookListSerializer(serializers.ModelSerializer):

    print 'third'
    fine = serializers.SerializerMethodField(source='get_fine')

    class Meta:
        print 'fourth'
        model = Books
        fields = ('ISBN', 'name', 'author', 'domain','fine')

    def get_fine(self, obj):

        print 'hell'

        return FineSerializer(instance=Fine.objects.filter(books_id=obj.id,student_id=self.context.get('c')),
                              many=True).data


class BookSecondSerializer(serializers.ModelSerializer):


    books = serializers.SerializerMethodField(source='get_books')

    class Meta:
        model = BookIssued
        fields = ('books','date_of_submission','date_of_issue')

    def get_books(self,obj):
        return BookListSerializer(instance=Books.objects.get(pk=obj.books_id),
                              context={'c': self.context.get('first_model_id')}).data


class StudentSerializer(serializers.ModelSerializer):

    print 'tenth'

    details = serializers.SerializerMethodField(source='get_details')

    class Meta:
        print '11'
        model = Student
        include = ('details')

    def get_details(self, obj):
        print 'first'
        return BookSecondSerializer(instance=BookIssued.objects.filter(student_id=obj.id),
                              many=True,context={'first_model_id': obj.id}).data

class  LoginDetailsLibrarySerializer(serializers.ModelSerializer):


    class Meta:
        model = LibraryAdmin
        fields = ('admin_id','name')


class  LoginDetailsStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('student_email','student_name')



