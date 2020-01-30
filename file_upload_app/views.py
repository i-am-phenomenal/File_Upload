from django.shortcuts import render
from .models import File, User_Profile
from .forms import FileForm, UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, Profile_Form
from playsound import playsound

# UTILITIES START
ALLOWED_FILE_TYPES = ['png', 'jpg', 'jpeg', 'mp3', 'wav']


def get_file_type(file):
    return file.music_file.url.split('.')[-1]

# UTILITIES END
# Create your views here.


def play_song(request):
    print("I AM HERE ")  # WIP
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        print("FORM ____________> ", form)
        if form.is_valid():
            # music_file = request.FILES['music_file']
            print("MUSIC FILE NAME ===> ", form.music_name)

        else:
            print("THE FORM IS NOT VALID ")

    return render(request, 'create.html', {})


def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.music_file = request.FILES['music_file']
            file_type = user_pr.music_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in ALLOWED_FILE_TYPES:
                return render(request, 'error.html', {})
            user_pr.save()
            all_files = User_Profile.objects.all()
            music_files = []
            for file in all_files:
                if get_file_type(file) == 'mp3':
                    music_files.append(file)
                else:
                    pass

            return render(request, 'details.html', {'user_pr': user_pr, 'music_files': music_files})

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
