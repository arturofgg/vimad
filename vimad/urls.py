from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'vimad_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vimad_app.urls', namespace='vimad_app')),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="vimad_app/accounts/reset_password.html"), name='reset_password'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(
        template_name="vimad_app/accounts/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="vimad_app/accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="vimad_app/accounts/password_reset_complete.html"), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
