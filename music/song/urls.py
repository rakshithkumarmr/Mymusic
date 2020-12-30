from django.urls import path

from song import views

urlpatterns = [
    path('',views.HomePage,name='home'),
    path('all_songs/', views.All_songs, name='all_songs'),
    path('songpost/<int:id>/', views.songpost, name='songpost'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('listen_later/', views.listen_later, name='listen_later'),
    path('ll_delete/<int:id>/',views.ll_delete,name='ll_delete'),
    path('history_delete/<int:id>/',views.history_delete,name='history_delete'),
    path('channel_song_delete/<int:id>/', views.channel_song_delete, name='channel_song_delete'),
    path('history/', views.history, name='history'),
    path('seacrh/', views.search, name='seacrh'),
    path('channel/', views.channel, name='channel'),
    path('upload_music/',views.upload_music,name='upload_music'),
    path('logout_user/',views.logout_user,name='logout_user')
]