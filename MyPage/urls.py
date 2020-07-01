from django.urls import path
from . import views as my_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', my_views.index, name='my-index'),
    path('register/', my_views.register, name='my-register'),
    path('profile/', my_views.profile, name='my-profile'),
    path('login/', auth_views.LoginView.as_view(template_name="MyPage/login.html"), name='my-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="MyPage/logout.html"), name='my-logout')
]
