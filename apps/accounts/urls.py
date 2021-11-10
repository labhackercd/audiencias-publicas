from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from audiencias_publicas.decorators import anonymous_required
from apps.accounts import views

urlpatterns = [
    path('login/', anonymous_required(auth_views.LoginView.as_view()),
         name='login'),
    path('logout/', login_required(auth_views.logout_then_login),
         name='logout'),
    path('signup/', anonymous_required(views.SignUpView.as_view()),
         name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
