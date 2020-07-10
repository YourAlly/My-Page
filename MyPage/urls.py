from django.urls import path
from . import views as my_views
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', my_views.PostsView.as_view(), name='my-index'),
    path('register/', my_views.register, name='my-register'),
    path('login/', my_views.LoginView.as_view(), name='my-login'),
    path('logout/', LogoutView.as_view(template_name="MyPage/logout.html"), name='my-logout'),
    path('contacts/', my_views.contacts, name='my-contacts'),
    path('contacts/message_user_id=<int:target_id>', my_views.send_message, name='my-messenger'),
    path('post/<int:post_id>/', my_views.post, name='my-post'),
    path('post/new/', my_views.post_form, name='my-new-post'),
    path('post/<int:post_id>/comment', my_views.process_comment, name='my-comment'),

    path('users/', my_views.users, name='my-users'),
    path('user/<int:user_id>/', my_views.user, name='my-user'),
    path('users/search/', my_views.user_search, name='my-search'),
    path('user/<int:user_id>/?action=<str:action>/', my_views.contact_action, name='my-contact-action'),
    
    path('user/changeimage/', my_views.update_image, name='my-update-image'),
    path('user/changeemail/', my_views.update_email, name='my-update-email'),

    path('user/<int:target_id>/chat/', my_views.chat, name='my-chat'),
    path('user/<int:target_id>/chat/send/',my_views.chat_send, name='my-chat-send'),
    path('user/<int:target_id>/chat/get/', my_views.chat_get, name='my-chat-get')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
