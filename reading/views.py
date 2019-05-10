from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
# Create your models here.

def index(request):
    resp = {'errorcode': 100, 'detail': 'Get success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")
# Create your views here.
