from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
# from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verification, PasswordView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, UserListView, deactivate_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password/', PasswordView.as_view(), name='password'),
    path('verification/', verification),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('users_list/', UserListView.as_view(), name='users_list'),
    path('deactivate_user/<int:pk>/', deactivate_user, name='deactivate_user'),
]
