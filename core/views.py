from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Timeset, Timeblock

# Create your views here.

class TimesetListView(ListView):
    model = Timeset
    template_name = "core/index.html"


class TimesetDetailView(DetailView):
    model = Timeset
    template_name = "core/timeset_detail.html"


