from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from voting_system.views import *

urlpatterns = [
    path('vote/', VoteView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
