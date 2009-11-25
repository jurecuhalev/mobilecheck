# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django import forms
from xlrd import open_workbook

class UploadForm(forms.Form):
  bill = forms.FileField()

def index(request):
  if request.method == 'POST': # If the form has been submitted...
      form = UploadForm(request.POST, request.FILES) # A form bound to the POST data
      if form.is_valid(): # All validation rules pass
          # Process the data in form.cleaned_data
          # ...
          process_bill(request.FILES['bill'])
          return HttpResponseRedirect('/thanks/') # Redirect after POST
  else:
      form = UploadForm() # An unbound form

  return render_to_response('index.html', {
      'form': form,
  })
    
    
    
def process_bill(bill):
  print bill



def main():
  aString = open('../samples/sample1.xls','rb').read()
  print open_workbook(file_contents=aString)

if __name__ == '__main__':
  main()