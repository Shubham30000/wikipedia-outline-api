"""
Wikipedia service module.
Handles fetching and parsing Wikipedia pages.
"""
from bs4 import BeautifulSoup
from typing import List, Tuple
from ..core.cache import cached_get

class WikipediaService:
    """Service for fetching and parsing Wikipedia pages."""
    
    BASE_URL = "https://en.wikipedia.org/wiki/"
    
    @staticmethod
    def construct_url(country: str) -> str:
        """
        Construct Wikipedia URL for a country.
        
        Args:
            country: Country name (e.g., "India", "United States")
            
        Returns:
            Full Wikipedia URL
        """
        # Replace spaces with underscores and capitalize first letter
        formatted_country = country.replace(" ", "_").title()
        return f"{WikipediaService.BASE_URL}{formatted_country}"
    
    @staticmethod
    def fetch_page(country: str) -> str:
        """
        Fetch Wikipedia page HTML for a country.
        
        Args:
            country: Country name
            
        Returns:
            HTML content as string
        """
        url = WikipediaService.construct_url(country)
        return cached_get(url)
    
    @staticmethod
    def extract_headings(html_content: str) -> List[Tuple[int, str]]:
        """
        Extract all headings (H1-H6) from HTML content IN DOCUMENT ORDER.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            List of tuples (level, text) where level is 1-6, in order of appearance
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        headings = []
        
        # Find all heading tags in document order
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            # Get the level from tag name (h1 -> 1, h2 -> 2, etc.)
            level = int(heading.name[1])
            
            # Get text content, stripping whitespace
            text = heading.get_text(strip=True)
            
            # Skip empty headings and remove [edit] links
            if text and '[edit]' not in text:
                text = text.replace('[edit]', '').strip()
                headings.append((level, text))
        
        return headings
    
    @classmethod
    def get_country_headings(cls, country: str) -> List[Tuple[int, str]]:
        """
        Fetch Wikipedia page and extract headings for a country.
        
        Args:
            country: Country name
            
        Returns:
            List of tuples (level, text)
        """
        html_content = cls.fetch_page(country)
        return cls.extract_headings(html_content)