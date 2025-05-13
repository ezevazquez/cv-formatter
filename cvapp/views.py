import json
from django.shortcuts import render
from .forms import CVUploadForm
from .utils import pdf_parser, openai_client, pdf_generator
import base64

def upload_cv(request):
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['file']
            texto = pdf_parser.extract_text_from_pdf(archivo)
            datos_estructurados = openai_client.structure_cv(texto)
            ruta_pdf = pdf_generator.generate_pdf(datos_estructurados)

            with open(ruta_pdf, 'rb') as f:
                pdf_base64 = base64.b64encode(f.read()).decode('utf-8')

            return render(request, 'cvapp/result.html', {
                'datos': datos_estructurados,
                'pdf_base64': pdf_base64,
            })
    else:
        form = CVUploadForm()
    return render(request, 'cvapp/upload.html', {'form': form})

