from django.urls import path

from . import views

app_name = 'information'
urlpatterns = [
    # Banner
    path('information/banners', views.BannersView.as_view(), name='banners'),

    # Donation
    path('information/donations', views.DonationsView.as_view(), name='donations'),
    path('information/donation', views.CreateDonationView.as_view(), name='donation_create'),
    path('information/donation/<int:donation_id>/download', views.DonationDownloadView.as_view(), name='donation_download'),

    # Calendar
    path('information/calendars/all', views.CalendarsAllView.as_view(), name='calendars_all'),
    path('information/calendars', views.CalendarsView.as_view(), name='calendars'),

    # History
    path('information/main/histories', views.MainHistoriesView.as_view(), name='information_main_histories'),
    path('information/affiliate/histories', views.AffiliateHistoriesView.as_view(), name='information_affiliate_histories'),

    # SocietyAbout
    path('society/abouts', views.SocietyAboutsView.as_view(), name='society_abouts'),

    # People
    path('intro/people', views.PeopleView.as_view(), name='intro_people'),

    # Information
    path('information', views.InformationView.as_view(), name='information'),

    # About
    path('intro/about', views.AboutView.as_view(), name='intro_about'),

    # ClinicAbout
    path('affiliate/clinic/about', views.ClinicAboutView.as_view(), name='clinic_about'),

]
