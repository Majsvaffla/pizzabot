from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from pb.events.views import Events


urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', Events.as_view()),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
