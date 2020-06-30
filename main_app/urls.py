from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='popular-movie/')),

    path('popular-movie/', views.imdbPopMovieView, name='imdbPopMovieView'),


    path('top-rated-movie/', views.imdbTopMovieView, name='imdbTopMovieView'),

    path('popular-tv/', views.imdbPopTvView, name='imdbPopTvView'),


    path('top-rated-tv/', views.imdbTopTvView, name='imdbTopTvView'),



]