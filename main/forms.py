from django import forms
from .models import Documents

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


#DataFlair #File_Upload
class Docs_Form(forms.ModelForm):
    class Meta:
        model = Documents
        fields = [
        'name',
        'data',
        'date'
        ]