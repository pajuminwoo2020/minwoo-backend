from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    ### User
    path('user/create', views.CreateUserView.as_view(), name='user_create'),
    path('user', views.UserView.as_view(), name='user'),
    path('user/login', views.UserLoginView.as_view(), name='login'),
    path('user/logout', views.UserLogoutView.as_view(), name='logout'),

    path('user/activate/<str:uidb64>/<str:token>', views.UserActivationView.as_view(), name='activate'),

    path('password/change', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/update/<str:uidb64>/<str:token>', views.PasswordUpdateView.as_view(), name='password_update'),

]
