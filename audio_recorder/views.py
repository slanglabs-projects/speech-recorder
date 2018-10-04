import uuid
import tempfile
import boto3
import os

from django.shortcuts import render
from django.views.decorators.http import require_POST

from .form import NameRegisterForm
from .models import *

from django.http import JsonResponse
from django.conf import settings


def register(request):

    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = NameRegisterForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data['name']
            try:
                user = User.objects.get(full_name=full_name)
            except User.DoesNotExist:
                user = User(full_name=full_name)
                user.save()
        else:
            return render(request, 'register.html', {'error': 'Please fill your full name'})

        return render(request, 'index.html', {'full_name': user.full_name})


def redirect_language(request):
    path = request.get_full_path().split('/')
    language = path[-2]
    full_name = path[-1]
    try:
        user = User.objects.get(full_name=full_name)
    except User.DoesNotExist:
        return render(request, 'register.html')

    if language == 'english':
        model = EnglishTranscipt
    elif language == 'hindi':
        model = HindiTranscipt
    else:
        model = TamilTranscipt

    transcript = model.objects.first()

    return render(request, 'base_language.html', {'full_name': user.full_name, 'transcript': transcript.text,
                                                'transcript_id': transcript.id})


def toggle_text(request):
    path = request.META.get('HTTP_REFERER').split('/')
    full_name = path[-1]
    language = path[-2]

    if full_name is None:
        return render(request, 'register.html')

    transcript_id = int(request.GET.get('transcript_id'))
    action = request.GET.get('action')

    if language == 'english':
        model = EnglishTranscipt
    elif language == 'hindi':
        model = HindiTranscipt
    else:
        model = TamilTranscipt

    count = model.objects.count()

    if action == 'prev' and 1 < transcript_id <= count:
        transcript_id -= 1
    elif transcript_id < count and action == 'next':
        transcript_id += 1

    transcript = model.objects.get(id=transcript_id)

    return JsonResponse({'full_name': full_name, 'transcript': transcript.text,
                         'transcript_id': transcript.id})


@require_POST
def save(request):
    language = request.META.get('HTTP_REFERER').split('/')[-2]
    full_name = request.POST.get('full_name')

    if full_name is None:
        return render(request, 'register.html')

    base64data = request.POST.get('base64data')

    transcript_text = request.POST.get('transcript_text')

    temp_file = tempfile.NamedTemporaryFile(prefix=str(uuid.uuid1()), suffix='.wav')

    temp_file.write(request.FILES.get('audio_data').read())

    temp_file.seek(0)

    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                      aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))

    file_name = temp_file.name.split('/')[-1]

    user = User.objects.get(full_name=full_name)

    key = os.path.join(language, file_name)

    s3.upload_file(temp_file.name, 'slangspeechdata', key)

    temp_file.flush()

    aws_link = settings.S3_PATH.format(file_name)
    speech_data = SpeechData(aws_link=aws_link, text=transcript_text,
                             user=user, base64=base64data)
    speech_data.save()

    return JsonResponse({})


def success(request):
    full_name = request.POST.get('full_name')
    if full_name is None:
        return render(request, 'register.html')

    user = User.objects.get(full_name=full_name)

    count = user.speech_data.values('text').distinct().count()

    return render(request, 'success.html', {'count': count, 'user': user.full_name})
