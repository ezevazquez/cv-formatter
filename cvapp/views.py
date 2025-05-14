from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm, CVUploadForm
from .utils import pdf_parser, openai_client, pdf_generator
from django.core.files.base import ContentFile
import base64
from django.shortcuts import render, redirect
from .forms import EmployeeForm

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

def employee_list(request):
    employees = Employee.objects.all().order_by('-last_updated')
    return render(request, 'cvapp/employee_list.html', {'employees': employees})

def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'cvapp/employee_detail.html', {'employee': employee})

def upload_cv(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = CVUploadForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            text = pdf_parser.extract_text_from_pdf(employee.uploaded_cv)
            structured = openai_client.structure_cv(text)
            employee.description = structured.get('description', '')
            employee.stack = structured.get('stack', [])
            employee.experience = structured.get('experience', [])
            employee.education = structured.get('education', [])
            pdf_path = pdf_generator.generate_pdf(structured)
            with open(pdf_path, 'rb') as f:
                content = ContentFile(f.read(), name=f'{employee.name}_cv.pdf')
                employee.generated_pdf.save(content.name, content, save=False)
            employee.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = CVUploadForm(instance=employee)
    return render(request, 'cvapp/employee_upload.html', {'form': form, 'employee': employee})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'cvapp/employee_create.html', {'form': form})