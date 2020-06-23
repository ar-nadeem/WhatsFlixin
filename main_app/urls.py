from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='popular/')),
    path('popular/', views.imdbPopMovieView, name='imdbPopMovieView'),
    path('top-rated/', views.imdbTopMovieView, name='imdbTopMovieView'),

]