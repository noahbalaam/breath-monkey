from django.urls import path
from . import views

urlpatterns = [
    path('', views.wimhof_home, name='wimhof_home'),
    path('create/', views.create_session, name='wimhof_create_session'),
    path('session/<int:session_id>/', views.session_detail, name='wimhof_session_detail'),
    path('stats/', views.view_stats, name='wimhof_stats'),
    path('save-stats/', views.save_stats, name='wimhof_save_stats'),
]