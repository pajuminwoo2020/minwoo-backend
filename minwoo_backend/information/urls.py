from django.urls import path

from . import views

app_name = 'information'
urlpatterns = [
        path('intro/location', views.IntroLocationView.as_view(), name='intro_location'),
        path('intro/people', views.PeopleView.as_view(), name='intro_people'),
                                
]
