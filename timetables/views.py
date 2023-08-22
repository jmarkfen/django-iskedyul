from django.http import HttpResponse 
from django.shortcuts import render
from fbv.decorators import render_html

# Create your views here.


@render_html() # index.html
def index(request):
    return {}
