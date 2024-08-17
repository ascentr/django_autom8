from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import color_style # style ur debug 
from PIL import Image
import io
from django.http import HttpResponse
from .forms import CompressForm


def compress(request):
  user = request.user
  style = color_style()

  if request.method == 'POST':
    form = CompressForm(request.POST, request.FILES)
    if form.is_valid():
      original_img = form.cleaned_data['original_img']
      quality = form.cleaned_data['quality']
      compressed_image  = form.save(commit=False)
      compressed_image.user = user

      #perform compression
      img = Image.open(original_img)
      output_format = img.format
      buffer = io.BytesIO()
      img.save(buffer, format=output_format, quality=quality)
      buffer.seek(0)
      # print(style.SUCCESS(f"Cursor position after compression: {buffer.tell()}"))

      #save the compressed image inside the model
      compressed_image.compressed_img.save(
        f'compressed_{original_img}' , buffer
      )
      #Automatically download the compressed file:
      response = HttpResponse(buffer.getvalue(), content_type=f'image/{output_format.lower()}')
      response['Content-Disposition'] = f'attachment; filename=compressed_{original_img}'
      return response
      messages.success(request, "Compression Successful ! Check downloads for compressed file")
      #
  else:
    form = CompressForm()

  context = {
    'form' : form, 
  }

  return render(request , 'image_compression/compress.html' , context)
