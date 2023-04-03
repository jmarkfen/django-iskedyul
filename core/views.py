from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import resolve, reverse, reverse_lazy
from django.views import generic as g
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from bootstrap_datepicker_plus.widgets import TimePickerInput
from .models import Timetable, Event
from . import oop

# Create your views here.

class TestView(g.TemplateView):
    template_name = "core/test.html"

class TimetableListView(ListView):
    model = Timetable
    template_name = "core/set_list.html"

class TimetableCreateView(CreateView):
    model = Timetable
    fields = "__all__"
    #template_name = ".html"

    def get_success_url(self):
        return reverse('set_list')

class TimetableDetailView(DetailView):
    model = Timetable
    template_name = "core/set_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['by_days'] = oop.day_dict(self.object.event_set.all())
        context['row_labels'] = self.object.get_time_ranges()
        context['rows'] = self.object.get_rows()
        context['matrix'] = self.object.get_matrix()
        return context
    

class TimetableUpdateView(UpdateView):
    model = Timetable
    fields = "__all__"
    #template_name = "core/set_form.html"

class TimetableDeleteView(DeleteView):
    model = Timetable
    #template_name = ".html"
    success_url = reverse_lazy('set_list')

# blocks

class EventCreateView(CreateView):
    model = Event
    fields = "__all__"
    #template_name = ".html"

    def get_initial(self):
        initial = super().get_initial()
        # set the value of the field to the 'set_id' url parameter
        initial['set'] = Timetable.objects.get(id=self.kwargs['set_id'])
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ## pass url parameter as context for template
        context['set_id'] = self.kwargs['set_id']
        return context
    

    def get_success_url(self):
        # sets/<int:pk>/
        return reverse('set_detail', kwargs={'pk': self.object.set_id,})

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
        return reverse('set_detail', kwargs={'pk': self.object.set_id})

class EventDeleteView(DeleteView):
    model = Event
    # template_name = ".html"

    def get_success_url(self):
        return reverse('set_detail', kwargs={'pk': self.object.set_id})
