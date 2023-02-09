from django.shortcuts import render
from django.views import generic as g

# Create your views here.

class TestView(g.TemplateView):
    template_name = "core/test.html"

