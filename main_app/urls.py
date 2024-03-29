from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ads.txt', views.AdsView, name='AdsView'),

    path('', RedirectView.as_view(url='movie/popular/')),
    path('popular-movie', RedirectView.as_view(url='movie/popular/')),

    path('movie', RedirectView.as_view(url='movie/popular/')),
    path('tv', RedirectView.as_view(url='tv/popular/')),


    path('movie/popular/', views.imdbPopMovieView, name='imdbPopMovieView'),
    path('movie/top-rated/', views.imdbTopMovieView, name='imdbTopMovieView'),

    path('tv/popular/', views.imdbPopTvView, name='imdbPopTvView'),
    path('tv/top-rated/', views.imdbTopTvView, name='imdbTopTvView'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)