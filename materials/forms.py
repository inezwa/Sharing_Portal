from django import forms
from .models import StudyMaterial, Rating, Comment
from django.core.exceptions import ValidationError 
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in settings.ALLOWED_FILE_EXTENSIONS:
        raise ValidationError(f'Unsupported file extension. Allowed: {", ".join(settings.ALLOWED_FILE_EXTENSIONS)}')
    

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),  # Display 1 to 5 as string
        }
        labels = {
            'rating': 'Rate this material (1-5)',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter material title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter material description'}),
            'file': forms.ClearableFileInput(),
            'category': forms.Select(),
        }
    def clean_file(self):
        file = self.cleaned_data.get('file')
        validate_file_extension(file)
        return file
    