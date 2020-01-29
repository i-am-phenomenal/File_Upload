from django import forms
from .models import File, User_Profile


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 MB'
    )


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["name", "filepath"]


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class Profile_Form(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = [
            'fname',
            'lname',
            'technologies',
            'email',
            'display_picture'
        ]
