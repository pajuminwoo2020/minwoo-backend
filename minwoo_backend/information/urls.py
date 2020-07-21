from django.urls import path

from . import views

app_name = 'information'
urlpatterns = [
    # Banner
    path('information/banners', views.BannersView.as_view(), name='banners'),

    # Donation
    path('information/donations', views.DonationsView.as_view(), name='donations'),
    path('information/donation', views.CreateDonationView.as_view(), name='donation_create'),

    # Calendar
    path('information/calendars/all', views.CalendarsAllView.as_view(), name='calendars_all'),
    path('information/calendars', views.CalendarsView.as_view(), name='calendars'),

    # History
    path('information/histories', views.InformationHistoriesView.as_view(), name='information_histories'),

    # SocietyAbout
    path('society/about/create', views.CreateSocietyAboutView.as_view(), name='society_about_create'),
    path('society/about/<int:society_about_id>', views.SocietyAboutView.as_view(), name='society_about'),
    path('society/abouts', views.SocietyAboutsView.as_view(), name='society_abouts'),
]
