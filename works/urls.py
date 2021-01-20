from django.urls import path, include
from .views import WorksView


urlpatterns = [
    path('works/', WorksView.as_view()),
]