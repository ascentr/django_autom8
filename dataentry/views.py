from django.shortcuts import render, redirect
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages
#local imports
from .utils import get_all_custom_models
from uploads.models import Upload

def importdata(request):
  if request.method=="POST":
    file_name = request.FILES.get('file_name')
    model_name = request.POST.get('model_name')

    upload = Upload.objects.create(file=file_name, model_name=model_name)
    retlative_path = str(upload.file.url)
    base_url = str(settings.BASE_DIR)
    file_path = base_url+retlative_path

    # trigger the importdata command
    try:
      call_command('importdata', file_path, model_name)
      messages.success(request, "Data Imported Successfully")
    except Exception as Err:
      messages.error(request, str(Err))      
    return redirect('importdata')

  else:
    custom_models = get_all_custom_models()
    context = { 'custom_models' : custom_models}
  return render(request, 'dataentry/importdata.html', context)
  
