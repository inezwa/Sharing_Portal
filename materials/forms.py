from django import forms
from .models import StudyMaterial,Rating, Comment

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3})
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = ['title', 'description', 'file', 'category']