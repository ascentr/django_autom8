from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
#local imports
from .utils import get_all_custom_models , check_csv_error
from uploads.models import Upload
from .tasks import import_data_task

def importdata(request):
  if request.method=="POST":
    file_name = request.FILES.get('file_name')
    model_name = request.POST.get('model_name')

    upload = Upload.objects.create(file=file_name, model_name=model_name)
    retlative_path = str(upload.file.url)
    base_url = str(settings.BASE_DIR)
    file_path = base_url+retlative_path

    #check for Errors
    try:
      check_csv_error(file_path, model_name)
    except Exception as e:
      messages.error(request, str(e))
      return redirect('importdata')

    #handle import_data task
    import_data_task.delay(file_path, model_name)
    messages.success(request, "Importing DATA, You will be notified when completed.")
    return redirect('importdata')
  else:
    custom_models = get_all_custom_models()
    context = { 'custom_models' : custom_models}

  return render(request, 'dataentry/importdata.html', context)
  
