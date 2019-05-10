from django.db import models
from django.http import HttpResponse
# Create your models here.

def index(request):
    resp = {'errorcode': 100, 'detail': 'Get success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")
