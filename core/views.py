from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Timeset, Timeblock

# Create your views here.

'''
Views for Timesets
'''

class TimesetListView(ListView):
    model = Timeset
    template_name = "core/index.html"


class TimesetDetailView(DetailView):
    model = Timeset
    template_name = "core/timeset_detail.html"


class TimesetCreateView(CreateView):
    model = Timeset
    template_name = ".html"


class TimesetUpdateView(UpdateView):
    model = Timeset
    template_name = ".html"


class TimesetDeleteView(DeleteView):
    model = Timeset
    template_name = ".html"

'''
Views for Timeblocks
'''

class TimeblockDetailView(DetailView):
    model = Timeblock
    template_name = "core/timeblock_detail.html"


class TimeblockCreateView(CreateView):
    model = Timeblock
    template_name = ".html"


class TimeblockUpdateView(UpdateView):
    model = Timeblock
    template_name = ".html"


class TimeblockDeleteView(DeleteView):
    model = Timeblock
    template_name = ".html"

