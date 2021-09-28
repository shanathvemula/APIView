import json

from rest_framework.views import APIView
import io
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q

from app.models import Employee
from app.serializers import EmployeeSerializer


@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCBV(APIView):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        #json_data = request
        stream = io.BytesIO(json_data)
        pdata = JSONParser().parse(stream)
        id = pdata.get('id', None)
        print(id)
        ename = pdata.get('ename',None)
        print(ename)
        sal = pdata.get('esal', None)
        print(sal)
        if id is not None:
            emp = Employee.objects.filter(Q(id=id)|Q(ename=ename)|Q(esal__gt=sal))
            print(emp)
            serializer = EmployeeSerializer(emp, many=True)
            print(serializer.data)
            json_data = JSONRenderer().render(serializer.data)
            print(json_data)
            return HttpResponse(json_data, content_type='application/json')
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return json_data
        #return HttpResponse(json_data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        #json_data = request.body
        json_data = request
        stream = io.BytesIO(json_data)
        pdata = JSONParser().parse(stream)
        serializer = EmployeeSerializer(data=pdata)
        if serializer.is_valid():
            serializer.save()
            msg = {'message': 'Data is added successfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def put(self, request, *args, **kwargs):
        #json_data = request.body
        json_data = request
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        emp = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(emp, data=data)
        if serializer.is_valid():
            serializer.save()
            msg = {'message': 'Data is updated successfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def patch(self, request, *args, **kwargs):
        #json_data = request.body
        json_data = request
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        print(id)
        emp = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(emp, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {'message': 'Data is updated successfully'}
            json_data = JSONRenderer().render(msg)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        #json_data = request.body
        json_data = request
        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)
        id = data.get('id')
        try:
            emp = Employee.objects.get(id=id)
            status, delete_item = emp.delete()
            if status == 1:
                msg = {'message': 'Resource deleted successfully'}
                json_data = JSONRenderer().render(msg)
                return HttpResponse(json_data, content_type='application/json')
            #return HttpResponse(json.dumps({'message': 'Unable to delete resource'}), content_type='application/json')
        except Employee.DoesNotExist:
            return HttpResponse(json.dumps({'message': 'Employee does not exits with this id'}), content_type='application/json')
