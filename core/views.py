from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def health(request):
    return HttpResponse('ok')

