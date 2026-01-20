"""
Outline service module.
Converts headings into Markdown-formatted outlines.
"""
from typing import List, Tuple

class OutlineService:
    """Service for generating Markdown outlines from headings."""
    
    @staticmethod
    def generate_markdown(headings: List[Tuple[int, str]]) -> str:
        """
        Generate Markdown outline from headings.
        
        Args:
            headings: List of tuples (level, text) where level is 1-6
            
        Returns:
            Markdown-formatted outline as string
        """
        if not headings:
            return ""
        
        markdown_lines = []
        
        for level, text in headings:
            # Create markdown heading with appropriate number of #
            # Level 1 = #, Level 2 = ##, etc.
            prefix = "#" * level
            markdown_lines.append(f"{prefix} {text}")
        
        return "\n\n".join(markdown_lines)
    
    @staticmethod
    def create_outline_with_header(country: str, headings: List[Tuple[int, str]]) -> str:
        """
        Create a complete outline with a header showing the country name.
        
        Args:
            country: Country name
            headings: List of tuples (level, text)
            
        Returns:
            Complete Markdown outline with header
        """
        markdown = OutlineService.generate_markdown(headings)
        
        # Add a header with the country name
        header = f"# Wikipedia Outline: {country.title()}\n\n"
        
        return header + markdown