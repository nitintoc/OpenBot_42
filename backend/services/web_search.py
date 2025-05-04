from typing import List, Dict
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

def search_web(keywords: str, max_results: int = 5) -> List[Dict]:
    """
    Perform a web search using DuckDuckGo for the given keywords.
    
    Args:
        keywords (str): The search query/keywords
        max_results (int): Maximum number of results to return (default: 5)
    
    Returns:
        List[Dict]: List of search results, where each result is a dictionary containing:
            - title: The title of the webpage
            - link: The URL of the webpage
            - snippet: A brief description of the webpage content
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(keywords, max_results=max_results))
            return results
    except Exception as e:
        print(f"Error performing web search: {str(e)}")
        return []

def extract_text_from_url(url: str, timeout: int = 10) -> Dict:
    """
    Extract text content from a given URL.
    
    Args:
        url (str): The URL to extract content from
        timeout (int): Request timeout in seconds
    
    Returns:
        Dict: Dictionary containing extracted information:
            - title: Page title
            - text: Main text content
            - status: HTTP status code
            - error: Error message if any
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get title
        title = soup.title.string if soup.title else "No title found"
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            'title': title,
            'text': text,
            'status': response.status_code,
            'error': None
        }
    except Exception as e:
        return {
            'title': None,
            'text': None,
            'status': getattr(e, 'response', {}).get('status_code', None),
            'error': str(e)
        }

def crawl_search_results(keywords: str, max_results: int = 5, delay: float = 1.0) -> List[Dict]:
    """
    Perform a web search and crawl through the results to extract content.
    
    Args:
        keywords (str): The search query/keywords
        max_results (int): Maximum number of results to process
        delay (float): Delay between requests in seconds to be respectful to servers
    
    Returns:
        List[Dict]: List of dictionaries containing search results and their content:
            - search_result: Original search result
            - content: Extracted content from the webpage
    """
    search_results = search_web(keywords, max_results)
    crawled_results = []
    
    for result in search_results:
        # Add delay between requests
        time.sleep(delay)
        
        url = result['link']
        content = extract_text_from_url(url)
        
        crawled_results.append({
            'search_result': result,
            'content': content
        })
    
    return crawled_results
