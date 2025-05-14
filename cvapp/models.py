from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    uploaded_cv = models.FileField(upload_to='uploads/', null=True, blank=True)
    generated_pdf = models.FileField(upload_to='generated_pdfs/', null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    description = models.TextField(blank=True)
    stack = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
