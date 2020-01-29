from django.shortcuts import render
from .models import File
from .forms import FileForm, UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, Profile_Form

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
# Create your views here.


def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.display_picture = request.FILES['display_picture']
            file_type = user_pr.display_picture.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                return render(request, 'error.html', {})
            user_pr.save()
            return render(request, 'details.html', {'user_pr': user_pr})

    context = {"form": form}
    return render(request, 'create.html', context)


def handle_uploaded_file(f):
    with open('C:/practice Programs/mario_theme.mp3', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('')
        else:
            form = UploadFileForm()
        return render(request, 'home.html', {'form': form})


def render_home(request):
    return render(request, 'home.html', {})


def showFile(request):
    print("+++++++++++++++++")
    # lastfile = File.objects.last()
    # filepath = lastfile.filepath
    # filename = lastfile.name

    form = FileForm(request.POST or None, request.FILE or None)
    if form.is_valid():
        form.save()

    context = {'filepath': "DUMMY FILE PATH",  # filepath,
               'form': form,
               'filename': "DUMMY FILE NAME "  # filename
               }

    return render(request, 'home.html', context)
