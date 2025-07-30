from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from monkeyusers.views import profile_view
from monkeyhome.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', welcome, name='welcome'),
    path('chat/', include('monkeychat.urls')),
    path('play/', include('monkeygame.urls')),
    path('profile/', include('monkeyusers.urls')),
    path('@<username>/', profile_view, name="profile"),
]

# Only used when DEBUG=True, whitenoise can serve files when DEBUG=False
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
