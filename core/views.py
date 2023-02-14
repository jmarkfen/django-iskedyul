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


# blocks

class BlockCreateView(CreateView):
    model = Block
    fields = "__all__"
    #template_name = ".html"

    def get_initial(self):
        initial = super().get_initial()
        # set the value of the field to the 'set_id' url parameter
        initial['set'] = Set.objects.get(id=self.kwargs['set_id'])
        return initial

    def get_success_url(self):
        # sets/<int:pk>/
        return reverse('set_detail', kwargs={'pk': self.object.set_id,})

class BlockUpdateView(UpdateView):
    model = Block
    fields = "__all__"
    # template_name = ".html"

    def get_success_url(self):
        return reverse('set_detail', kwargs={'pk': self.object.set_id})