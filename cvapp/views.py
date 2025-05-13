from django.shortcuts import render
from .forms import CVUploadForm

def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['file']
            # Por ahora solo mostramos el nombre del archivo subido
            return render(request, 'cvapp/result.html', {'archivo_nombre': archivo.name})
    else:
        form = CVUploadForm()
    return render(request, 'cvapp/upload.html', {'form': form})
