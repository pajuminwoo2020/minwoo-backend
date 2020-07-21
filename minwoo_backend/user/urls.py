from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "user"
urlpatterns = [
    ### User
    path('user/create', views.CreateUserView.as_view(), name='user_create'),
    path('user', views.UserView.as_view(), name='user'),
    path('user/login', views.UserLoginView.as_view(), name='login'),
    path('user/logout', views.UserLogoutView.as_view(), name='logout'),

    path('user/activate/<str:uidb64>/<str:token>', views.UserActivateView.as_view(), name='activate'),
    path('password/reset', views.PasswordResetView.as_view(), name='password_reset'),

    #path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
