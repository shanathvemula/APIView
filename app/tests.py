from django.test import TestCase

# Create your tests here.
from .views import *


class EmployeeTestCase(TestCase):
    def setUp(self):
        print('setUp')
        Employee.objects.create(eno=110, ename="Shanath", esal=129000.34, eaddr='ATM')
        Employee.objects.create(eno=111, ename="Shanath", esal=12000.34, eaddr='ATM')

    def test_Employee_Info(self):
        print("Test Case")
        qs = Employee.objects.all()
        serializer = EmployeeSerializer(qs, many=True)
        json_data = JSONRenderer().render(serializer.data)
        s = EmployeeCBV.get(self, request=b'{}')
        self.assertEqual(json_data, s)

    def test_Employee_status(self):
        s = EmployeeCBV.get(self, request=b'{"id":1}')
        self.assertEqual(s.status_code, 200)

    def test_Employee_post(self):
        s = EmployeeCBV.post(self,request=b'{"eno":112,"ename":"Shanath","esal":120000.76,"eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_post_error(self):
        s = EmployeeCBV.post(self,request=b'{"eno":112,"esal":120000.76,"eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_put(self):
        s = EmployeeCBV.put(self,request=b'{"id":2,"eno":112,"ename":"Shanath","esal":120000.76,"eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_put_error(self):
        s = EmployeeCBV.put(self,request=b'{"id":2,"ename":"Shanath","esal":120000.76,"eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_patch(self):
        s = EmployeeCBV.patch(self,request=b'{"id":2,"esal":12000.76,"eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_patch_error(self):
        s = EmployeeCBV.patch(self,request=b'{"id":2,"esal":"Ten","eaddr":"KURNOOL"}')
        self.assertEqual(s.status_code,200)

    def test_Employee_delete(self):
        s = EmployeeCBV.delete(self, request=b'{"id":2}')
        self.assertEqual(s.status_code, 200)

    def test_Employee_delete_error(self):
        s = EmployeeCBV.delete(self, request=b'{"id":100000}')
        self.assertEqual(s.status_code, 200)
