from django import forms
<<<<<<< HEAD
from django.core.exceptions import ValidationError
import os
=======
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
<<<<<<< HEAD
        fields = ['name', 'resume_file']

    def clean_resume_file(self):
        file = self.cleaned_data.get('resume_file')
        if file:
            # Validate size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("File size must not exceed 5MB.")
            
            # Validate extension
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in ['.pdf', '.docx']:
                raise ValidationError("Only PDF and DOCX files are allowed.")
        return file
=======
        fields = ['name', 'resume_file']
>>>>>>> 635a5accff9886b6cff2d9131f8795ff9c435487
