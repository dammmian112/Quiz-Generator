from django.urls import path
from .views import QuizGeneratorView

urlpatterns = [
    path('generate-quiz/', QuizGeneratorView.as_view(), name='generate_quiz'),
]
