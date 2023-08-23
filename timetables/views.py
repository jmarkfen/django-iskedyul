from django.http import HttpResponse 
from django.shortcuts import render
from fbv.decorators import render_html

# Create your views here.


@render_html()
def index(request):
    return {}


@render_html()
def page(request, id):
    return {}


@render_html()
def create_form(request):
    # return create_form
    return {}


@render_html()
def edit_form(request, id):
    # return edit form
    return {}


@render_html()
def delete_dialog(request, id):
    # return delete confirmation dialog
    return {}


def create(request):
    # create model
    # return success or fail
    return {}


def read(request, id):
    # get model
    # return json
    return {}


def update(request, id):
    # update model
    # return success or fail
    return {}


def delete(request, id):
    # delete model
    # return success or fail
    return {}


@render_html()
def event_create_form(request):
    # return create_form
    return {}


@render_html()
def event_edit_form(request, id):
    # return edit form
    return {}


@render_html()
def event_delete_dialog(request, id):
    # return delete confirmation dialog
    return {}


def event_create(request, id):
    # get model
    # return json
    return {}


def event_read(request, id):
    # get model
    # return json
    return {}


def event_update(request, id):
    # update model
    # return success or fail
    return {}


def event_delete(request, id):
    # delete model
    # return success or fail
    return {}