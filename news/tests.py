from django.test import TestCase
from models import user

# Create your tests here.
def testDb():
    tmp = user.objects.filter().filter(openid="dyx")
    print(tmp)