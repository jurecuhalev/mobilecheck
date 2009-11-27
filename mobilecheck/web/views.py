# -*- coding: utf-8 -*-
import time
from django.shortcuts import render_to_response
from django import forms

from django.conf import settings
from mobilecheck.utils import simobil


class UploadForm(forms.Form):
  racun = forms.FileField()

def index(request):
  def _save_file(onlinefile):
    f = open(settings.UPLOADS_DIR+str(time.time())+'_'+onlinefile.name, 'wb')
    f.write(onlinefile.read())
    f.close()
  
    return settings.UPLOADS_DIR+str(time.time())+'_'+onlinefile.name
  
  if request.method == 'POST': # If the form has been submitted...
      form = UploadForm(request.POST, request.FILES) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          if settings.KEEPFILES:
            storedfile = _save_file(request.FILES['racun'])
          request.FILES['racun'].seek(0)
          storedfile = request.FILES['racun']
          
          print storedfile
          summary = simobil.process(storedfile)
          return render_to_response('processed.html',
                                    {'summary': summary})
  else:
      form = UploadForm() # An unbound form

  return render_to_response('index.html', {
      'form': form,
  })
