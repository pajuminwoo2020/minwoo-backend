from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    ### User
    path('user/create', views.CreateUserView.as_view(), name='user_create'),
    path('user', views.UserView.as_view(), name='user'),
    path('user/login', views.UserLoginView.as_view(), name='login'),
    path('user/logout', views.UserLogoutView.as_view(), name='logout'),
]
