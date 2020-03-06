from django.shortcuts import render, redirect
from .models import File, User_Profile
from django.urls import reverse
from .forms import FileForm, UploadFileForm
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, Profile_Form
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound
import logging
import traceback 
from file_upload.settings import MEDIA_ROOT
import uuid
import subprocess 

# UTILITIES START
ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'mp3', 'wav', 'aac', 'amr']

def get_file_type(file):
    return file.music_file.url.split('.')[-1]

def convert_name_to_wav(filename):
    return filename.split('.')[0] + '.wav'
    
# C:\django_projects\File_Upload\media/mp3_test.mp3

def return_formatted_name(filename): 
    splitted = filename.split('media')
    sliced_name = splitted[1][1:]
    return splitted[0] + '/media/' + sliced_name

# UTILITIES END

# Create your views here.

def play_song(request):
    file_uuid=request.POST.get("file_uuid")
    fetched =  User_Profile.objects.get(uuid=file_uuid)
    filename = MEDIA_ROOT + str(fetched.music_file)
    formatted_filename = return_formatted_name(filename)
    print(formatted_filename, "   FORMATTED FILE NAME ")
    song = AudioSegment.from_mp3(formatted_filename)
    play(song)
    # try:
    #     print(formatted_filename, "******* FILE NAME *******")
    #     subprocess.call(['ffmpeg', '-i', formatted_filename,
    #                convert_name_to_wav(formatted_filename)])
        # audio = AudioSegment.from_mp3(filename)
        # audio.export(return_formatted_name(filename), format="wav")
        #  playsound(MEDIA_ROOT + str(fetched.music_file))
    # except Exception as e: 
    #     logging.error(traceback.format_exc())


    # wave_object = sa.WaveObject.from_wave_file(filename)
    # play_object = wave_object.play()
    # play_object.wait_done()
    # file = AudioSegment.from_wav(MEDIA_ROOT + str(fetched.music_file))
    # play(file)
    # playsound(MEDIA_ROOT + str(fetched.music_file))


    all_records = User_Profile.objects.all()
    
    return redirect('/list_all', {'music_files': all_records})

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
