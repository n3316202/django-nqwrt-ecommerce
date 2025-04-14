from django.test import TestCase

# Create your tests here.


def add(num1, num2):
    return num1 + num2


def minus(num1, num2):
    return num1 - num2


dic_calculator = {
    "add/": add,
    "minus/": minus,
}


class AnyTest(TestCase):
    def setUp(self):
        pass

    def test_calculator(self):
        url = "add/"
        print(url)
        print(dic_calculator[url](3, 2))
