from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.views import generic as g
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from bootstrap_datepicker_plus.widgets import TimePickerInput
from .models import Timetable, Event, WeekDays
from . import oop

# Create your views here.

class TestView(g.TemplateView):
    template_name = "core/test.html"

class TableListView(ListView):
    model = Timetable
    template_name = "core/timetable_list.html"

class TableCreateView(CreateView):
    model = Timetable
    fields = "__all__"
    #template_name = ".html"

    def get_success_url(self):
        return reverse('table_list')

class TableDetailView(DetailView):
    model = Timetable
    template_name = "core/timetable_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['by_days'] = oop.day_dict(self.object.event_set.all())
        context['row_labels'] = self.object.get_time_ranges()
        context['rows'] = self.object.get_rows()
        matrix = self.object.get_matrix()
        context['matrix'] = matrix
        tb = []
        # matrix[column][subcolumn][row]
        context['tb'] = tb
        context['row_count'] = range(5)
        return context
    

class TableUpdateView(UpdateView):
    model = Timetable
    fields = "__all__"
    #template_name = "core/set_form.html"

class TableDeleteView(DeleteView):
    model = Timetable
    #template_name = ".html"
    success_url = reverse_lazy('table_list')

# blocks

class EventCreateView(CreateView):
    model = Event
    fields = "__all__"
    #template_name = ".html"

    # modify generated form
    def get_form(self):
        form = super().get_form()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput()
        # set selected timetable
        form.fields['timetable'].initial = self.kwargs['set_id']
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ## pass url parameter as context for template
        context['set_id'] = self.kwargs['set_id']
        return context
    

    def get_success_url(self):
        # sets/<int:pk>/
        return reverse('table_detail', kwargs={'pk': self.object.set_id,})

class EventUpdateView(UpdateView):
    model = Event
    fields = "__all__"
    # template_name = ".html"

    # modify generated form
    def get_form(self):
        form = super().get_form()
        form.fields['start_time'].widget = TimePickerInput()
        form.fields['end_time'].widget = TimePickerInput(range_from='start_time')
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ## pass url parameter as context for template
        context['set_id'] = self.kwargs['set_id']
        return context

    def get_success_url(self):
        return reverse('table_detail', kwargs={'pk': self.object.set_id})

class EventDeleteView(DeleteView):
    model = Event
    # template_name = ".html"

    def get_success_url(self):
        return reverse('table_detail', kwargs={'pk': self.object.set_id})
