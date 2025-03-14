from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .wiki_api import get_article_content
from .utils import generate_quiz
import logging

logger = logging.getLogger(__name__)

class QuizGeneratorView(APIView):
    def get(self, request):
        topic = request.GET.get('topic')
        logger.info(f"Received request for topic: {topic}")
        
        if not topic:
            logger.error("No topic provided")
            return Response({'error': 'Topic is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            article_content = get_article_content(topic)
            logger.info(f"Article content retrieved: {article_content[:100]}...")
            
            if not article_content:
                logger.error(f"No article found for topic: {topic}")
                return Response({'error': 'Nie znaleziono artykułu dla podanego tematu'}, status=status.HTTP_404_NOT_FOUND)
            
            quiz = generate_quiz(article_content)
            logger.info(f"Generated quiz with {len(quiz)} questions")
            return Response({'questions': quiz}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return Response({'error': f'Wystąpił błąd: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        topic = request.data.get('topic')
        logger.info(f"Received POST request for topic: {topic}")
        
        if not topic:
            logger.error("No topic provided in POST request")
            return Response({'error': 'Topic is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            article_content = get_article_content(topic)
            logger.info(f"Article content retrieved: {article_content[:100]}...")
            
            if not article_content:
                logger.error(f"No article found for topic: {topic}")
                return Response({'error': 'Nie znaleziono artykułu dla podanego tematu'}, status=status.HTTP_404_NOT_FOUND)
            
            quiz = generate_quiz(article_content)
            logger.info(f"Generated quiz with {len(quiz)} questions")
            return Response({'questions': quiz}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return Response({'error': f'Wystąpił błąd: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
