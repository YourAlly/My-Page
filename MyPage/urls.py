from django.urls import path
from . import views as my_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', my_views.index, name='my-index'),
    path('register/', my_views.register, name='my-register'),
    path('contacts/', my_views.contacts, name='my-contacts'),
    path('post=<int:pk>/', my_views.PostDetailView.as_view(), name='my-post'),

    path('user/<int:user_id>/', my_views.user, name='my-user'),
    path('user/<int:user_id>/add/', my_views.add, name='my-add'),
    path('user/<int:user_id>/remove/', my_views.remove, name='my-remove'),
    

    path('user/changeimage/', my_views.update_image, name='my-update-image'),
    path('user/changeemail/', my_views.update_email, name='my-update-email'),

    path('login/', auth_views.LoginView.as_view(template_name="MyPage/login.html"), name='my-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="MyPage/logout.html"), name='my-logout')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
