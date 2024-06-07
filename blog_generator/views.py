from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from pytube import YouTube

import os
import json
import openai
import logging
import assemblyai as aai
# Create your views here.
logger = logging.getLogger(__name__)



@login_required
def index(request):    
    return render(request, "index.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)            
            return redirect('/')
        else:
            error_message = "invalid email or password"
            return render(request, "login.html", {'error_message': error_message})
        
    return render(request, 'login.html',   )

def user_signup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password == repassword:
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                login(request, user)
                return redirect('/',{user})
            except Exception as e:
                logger.error(f"Error creating user:{e}")
                return render(request, 'signup.html', {'error_message': 'error creating user'})
        else:
            error_message = "Password does not match"
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data =  json.loads(request.body)
            yt_link = data['link']
            yt = YouTube(yt_link)  
            yt_title =yt.title
            yt_thumbnail = yt.thumbnail_url
            qual, stream, size =[],[],[]
            # print(yt_info)
            for vid in yt.streams.filter(adaptive=True,  subtype='mp4'):
                if vid.resolution is not None:
                    qual.append(vid.resolution)
                    stream.append(vid)
                    mb =int(vid.filesize_mb)  
                    size.append(str(mb) +'mb')
                
                
                context = {'vid_title': yt_title, 'vid_thumbnail':yt_thumbnail, 'qual':qual, 'size':size , 'yt_link':yt_link}
            # print(qual, size)
           # print(stream)
            return JsonResponse({'vid_title': yt_title, 'vid_thumbnail':yt_thumbnail, 'qual':qual, 'size':size , 'yt_link':yt_link})
            
        except(KeyError, json.JSONDecodeError):
            return JsonResponse({'error':'invaid data method'}, status = 400)
        
        #get title
        
        title = yt_title(yt_title)
    else:
        return JsonResponse({'error':'invaid request method'}, status = 405)
    

@csrf_exempt
def qualitylink(request):
    print('hello')
    if request == 'POST':
        print('true')
        quality = request.POST['quality']
        print(quality)
        return JsonResponse({'value':'download started'})
    else:
        return JsonResponse({'error':'invaid request method'}, status = 405)

def get_audio(link):
    yt = YouTube(link)
    audio = yt.streams.filter(only_audio='True').first()
    out_file = audio.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + 'mp4'
    os.rename(out_file, new_file)
    print(new_file)
    return new_file

def get_video(link):
    yt = YouTube(link)
    # streams = set ()
    resolutions = []
    for i in yt.streams.filter(progressive='True'):
        resolutions.append(i.resolution)

    resolutions.sort()
    for res in resolutions:
        print(res)
    # video = yt.streams.filter(resolution='mp4' ).first()
    # video.download(output_path=settings.MEDIA_ROOT)
    # video = yt.streams.filter(only_video='True').first()
    # out_file = video.download(output_path=settings.MEDIA_ROOT)
    # base, ext = os.path.splitext(out_file)
    # new_file = base + 'mp4'
    # os.rename (out_file, new_file)
    # print(new_file)
    return res


# def get_transcription(link):
#     audio_file = get_audio(link)
#     aai.settings.api_key ='3d240f81898c45eaa27cf37f859391ff'
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(audio_file)
#     print(transcriber.text)
#     return transcriber.text

