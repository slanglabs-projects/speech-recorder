from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', register, name='register'),
    url(r'^save$', save, name='save'),
    url(r'^hindi/?', redirect_language, name='hindi'),
    url(r'^english/?', redirect_language, name='english'),
    url(r'^tamil/?', redirect_language, name='tamil'),
    url(r'^toggle/?', toggle_text, name='toggle'),
    url(r'^success$', success, name='success'),
]
