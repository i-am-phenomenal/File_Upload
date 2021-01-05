from django.shortcuts import render, redirect
from .models import File, User_Profile
from django.urls import reverse
from .forms import FileForm, UploadFileForm
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, Profile_Form
import simpleaudio as sa
from pydub import AudioSegment 
from pydub.playback import play
import logging
import traceback 
from file_upload.settings import MEDIA_ROOT
import uuid
import os
import pydub
import scipy
import scipy.io.wavfile
import tempfile
from django.contrib import messages


# UTILITIES START

ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'mp3', 'wav', 'aac', 'amr']

def log_exception():
    logging.error(traceback.format_exc())

def get_file_type(file):
    return file.music_file.url.split('.')[-1]


    """
    Read an MP3 File into numpy data.
    :param file_path: String path to a file
    :param as_float: Cast data to float and normalize to [-1, 1]
    :return: Tuple(rate, data), where
        rate is an integer indicating samples/s
        data is an ndarray(n_samples, 2)[int16] if as_float = False
            otherwise ndarray(n_samples, 2)[float] in range [-1, 1]
    """
def convert_to_arr(filename, as_float = False): 
    path, extension = os.path.splitext(filename)
    assert extension == '.mp3'
    mp3 = pydub.AudioSegment.from_mp3(filename)
    _, path = tempfile.mkstemp()
    mp3.export(path, format='wav')
    rate, data = scipy.io.wavfile.read(path)
    try: 
        os.remove(path) # Files at this path needs to be deleted(will do in future commits probably).
    except Exception as _:
        log_exception()

    if as_float:
        data = data/(2**15)

    return rate, data

def return_all_music_records():
    return User_Profile.objects.all()

def return_file_uuid(request_object):
    return request_object.POST.get("file_uuid")

# UTILITIES END

# Create your views here.

def pause_current_music(request):
    file_uuid = return_file_uuid(request)
    fetched = User_Profile.objects.get(uuid=file_uuid)
    # wip    
    return render(request, 'details.html', {'music_files': return_all_music_records()})

def play_song(request):
    file_uuid = return_file_uuid(request)
    fetched =  User_Profile.objects.get(uuid=file_uuid)
    # print(type(fetched.music_file), "00000000000000")
    # print(type(str(fetched.music_file)), "1111111111111111")
    filename = MEDIA_ROOT + str(fetched.music_file)
    # print(filename, "2222222222222222222")
    rate, data = convert_to_arr(filename, False)
    try:  
        audio_object = sa.play_buffer(data, 2, 2, 44100) # There are some changes in the pitch and tempo whne using this method. Need to look into this
        if audio_object.is_playing():
            messages.success(request, 'True')
    except Exception as _: 
        log_exception()

    return redirect('/list_all', {'music_files': return_all_music_records()})

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
            object, created = User_Profile.objects.get_or_create(music_file= request.FILES['music_file'], music_name=user_pr.music_name, extension=file_type )
    
            music_files = []
            for file in User_Profile.objects.all():
                music_files.append(file)

            return render(request, 'details.html', {'music_files': music_files})

    context = {"form": form}
    return render(request, 'create.html', context)


def handle_uploaded_file(f):
    with open('C:/practice Programs/mario_theme.mp3', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def list_all_files(request): 
    all_files = User_Profile.objects.all()
    return render(request, 'details.html', {'music_files': all_files})

def delete_all_files(request): 
    try: 
        User_Profile.objects.all().delete()
        return render(request, 'all_deleted.html')
    except:
        print("THERE WAS AN ERROR WHILE TRYING TO DELETE RECORDS")
        return render(request, 'error.html', {})
    

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
    form = FileForm(request.POST or None, request.FILE or None)
    if form.is_valid():
        form.save()

    context = {'filepath': "DUMMY FILE PATH",  # filepath,
               'form': form,
               'filename': "DUMMY FILE NAME "  # filename
               }

    return render(request, 'home.html', context)
