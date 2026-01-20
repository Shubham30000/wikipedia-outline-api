"""
Wikipedia service module.
Handles fetching and parsing Wikipedia pages.
"""
from lxml import html
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
        tree = html.fromstring(html_content)
        headings = []
        
        # Extract ALL headings in document order using XPath
        # This gets h1, h2, h3, h4, h5, h6 in the order they appear
        all_headings = tree.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6')
        
        for heading in all_headings:
            # Get the tag name (h1, h2, etc.)
            tag_name = heading.tag.lower()
            
            # Extract the level number (1 from 'h1', 2 from 'h2', etc.)
            level = int(tag_name[1])
            
            # Get text content, stripping whitespace
            text = heading.text_content().strip()
            
            # Skip empty headings and edit links
            if text and '[edit]' not in text:
                # Remove [edit] from text if present
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