from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='popular/')),
    path('popular/', views.PopView, name='PopView'),
    path('top-rated/', views.TopView, name='TopView'),

]