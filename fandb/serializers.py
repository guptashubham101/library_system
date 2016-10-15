from rest_framework import serializers

from fandb.models import Student,BookIssued,Books,LibraryAdmin,Fine

class FineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fine
        fields = ('is_paid','days','amount')

class StudentListSerializer(serializers.ModelSerializer):

    fine = serializers.SerializerMethodField(source='get_fine')

    class Meta:
        model = Student
        fields = ('student_name', 'student_roll_number', 'student_email', 'branch','semester','year','fine')

    def get_fine(self, obj):
        return FineSerializer(instance=Fine.objects.filter(student_id=obj.id),
                              many=True).data

class BookSerializer(serializers.ModelSerializer):
    student = StudentListSerializer()
    class Meta:
        model = BookIssued
        fields = ('student','date_of_submission','date_of_issue')

class BookDetailsSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField(source='get_details')
    class Meta:
        model=Books

        include = ('details')

    def get_details(self, obj):

        return BookSerializer(instance=BookIssued.objects.filter(books_id=obj.id),
                                    many=True).data

class BookListSerializer(serializers.ModelSerializer):

    fine = serializers.SerializerMethodField(source='get_fine')

    class Meta:
        model = Books
        fields = ('ISBN', 'name', 'author', 'domain','fine')

    def get_fine(self, obj):
        return FineSerializer(instance=Fine.objects.filter(books_id=obj.id),
                              many=True).data


class BookSecondSerializer(serializers.ModelSerializer):

    books = BookListSerializer()
    class Meta:
        model = BookIssued
        fields = ('books','date_of_submission','date_of_issue')


class StudentSerializer(serializers.ModelSerializer):

    details = serializers.SerializerMethodField(source='get_details')

    class Meta:
        model = Student
        include = ('details')

    def get_details(self, obj):

        return BookSecondSerializer(instance=BookIssued.objects.filter(student_id=obj.id),
                              many=True).data

class  LoginDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryAdmin
        fields = ('admin_id','name')



