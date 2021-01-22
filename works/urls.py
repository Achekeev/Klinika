from django.urls import path, include
from .views import WorksView, BlogsView, AsksView, FeedbackView, OnlineView


urlpatterns = [
    path('works/', WorksView.as_view()),
    path('blogs/', BlogsView.as_view()),
    path('asks/', AsksView.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path('online/', OnlineView.as_view()),
]