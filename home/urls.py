from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('new/', newbreath_view, name='new'),
    path('newbreath/', newbreath_view, name='newbreath'),
    path('reggae/', toggle_reggae, name='reggae'),
    path('stats/', breathing_stats, name='breathing_stats'),
    path('record-session/', record_breathing_session, name='record_breathing_session'),

]