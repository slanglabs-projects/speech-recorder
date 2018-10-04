from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('audio_recorder.urls', namespace='voice_recorder')),
]
