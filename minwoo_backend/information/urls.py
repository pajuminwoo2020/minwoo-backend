from django.urls import path

from . import views

app_name = 'information'
urlpatterns = [
    # Banner
    path('information/banners', views.BannersView.as_view(), name='banners'),
    # History
    path('information/histories', views.InformationHistoriesView.as_view(), name='information_histories'),
]
