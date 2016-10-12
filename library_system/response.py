from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, search=None, **kwargs):

        # In case of search we don't need to json render
        if search:
            content = data
        else:
            content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


VALIDATION_ERROR_MESSAGE = {"result": False, "message": "Validation error occurred!"}

OBJECT_DOES_NOT_EXIST = {"result": False, "message": "Object does not exist!"}

SUCCESS_MESSAGE = {"result": True}

ERROR_MESSAGE = {"result": False}

FACULTY_NOT_AUTHORIZED = {'result': False, 'details': 'This faculty is not authorized to perform this action'}

UNAUTHORIZED = {'result':False,'details':'The user is not authorized to access'}