from django.shortcuts import render
from .models import File, User_Profile
from .forms import FileForm, UploadFileForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, Profile_Form
from playsound import playsound
import logging
import traceback 
import uuid

# UTILITIES START
ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'mp3', 'wav', 'aac', 'amr']


def get_file_type(file):
    return file.music_file.url.split('.')[-1]

def check_if_music_file_exists(file_name):
    try: 
        User_Profile.objects.get(music_name=file_name)
        return True 
    except User_Profile.DoesNotExist: 
        return False
    # formatted = file_name.
    # formatted_name = file_name.url.split('.')[0].split('/')[-1]
    # print(file_name, "FORMATTED NAME ")
    # for file in User_Profile.objects.all():
    #     print(file.music_name, "FILE NAME ")
    # try: 
    #     User_Profile.objects.get(music_name=file_name)
    #     print('********** RECORD EXISTS **********')
    # except User_Profile.DoesNotExist: 
    #     logging.error(traceback.format_exc())
    #     return False
    # object, created = User_Profile.get_or_create(music_name=file_name)
    # if created:
    #     return False
    # else: 
    #     return True
    # print(file_name, " DDDDDDDDDDDDDDDDDDDD")
    # try:
    #     fetched = User_Profile.objects.get(music_name=file_name)
    #     print(fetched.music_name, "FETCHED ----> ")
    #     return True
    # except Exception as e:
    #     logging.error(traceback.format_exc())



# UTILITIES END
# Create your views here.


def play_song(request):
    return render(request, 'create.html', {})

def create_profile(request):
    form = Profile_Form()
    if request.method == 'POST':
        form = Profile_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.music_file = request.FILES['music_file']
            print(request.FILES['music_file'], " ",  user_pr.music_file, " ", user_pr.music_name, "&&&&&&&&&&&&&&&&&&&&")
            # user_pr.uuid = uuid.uuid4()
            file_type = user_pr.music_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in ALLOWED_FILE_TYPES:
                return render(request, 'error.html', {})
            object, created = User_Profile.objects.get_or_create(music_file= request.FILES['music_file'], music_name=user_pr.music_name, extension=file_type )
            if created:
                print("RECORD CREATED SUCCESSFULLY !!!", object.music_name, " ", object.extension, ' ')
            music_files = []
            for file in User_Profile.objects.all():
                print(file.music_name, " ", type(file), "")
                music_files.append(file)

            # music_files = []
            # for file in all_files:
            #     music_files.append(file)
                # if get_file_type(file) == 'mp3':
                #     music_files.append(file)
                # else:
                #     pass

            return render(request, 'details.html', {'music_files': music_files}) #music_files})

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
        print("ALL RECORDS SUCCESSFULLY DELETED !!")
    except:
        print("THERE WAS AN ERROR WHILE TRYING TO DELETE RECORDS")
    
    return render(request, 'home.html')

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
