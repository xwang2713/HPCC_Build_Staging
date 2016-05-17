# Create your views here.
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, RequestContext
#from django.utils import simplejson
from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import Select
import simplejson


import os
import sys

def index(request):
    response_dict = {}

    if not request.POST:
        return render_to_response('LocalStageListing/index.html',
        response_dict, context_instance=RequestContext(request))
