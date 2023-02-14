from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.views import generic as g
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Set, Block

# Create your views here.

class TestView(g.TemplateView):
    template_name = "core/test.html"

class SetListView(ListView):
    model = Set
    template_name = "core/set_list.html"

class SetCreateView(CreateView):
    model = Set
    fields = "__all__"
    #template_name = ".html"

    def get_success_url(self):
        return reverse('set_list')

class SetDetailView(DetailView):
    model = Set
    template_name = "core/set_detail.html"

class SetUpdateView(UpdateView):
    model = Set
    fields = "__all__"
    #template_name = "core/set_form.html"
