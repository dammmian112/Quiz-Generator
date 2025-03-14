import requests
import logging

logger = logging.getLogger(__name__)

def get_article_content(topic):
    """
    Pobiera artykuł z Wikipedia na podstawie tematu.
    """
    endpoint = "https://pl.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True,
        'titles': topic,
    }
    
    try:
        logger.info(f"Fetching article for topic: {topic}")
        response = requests.get(endpoint, params=params)
        logger.info(f"Wikipedia API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch article. Status code: {response.status_code}")
            return None
        
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        
        for page_id, page in pages.items():
            if 'extract' in page:
                content = page['extract']
                logger.info(f"Successfully retrieved article content. Length: {len(content)}")
                return content
                
        logger.error("No article content found in the response")
        return None
        
    except Exception as e:
        logger.error(f"Error fetching article: {str(e)}")
        return None
