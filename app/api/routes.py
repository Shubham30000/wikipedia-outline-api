"""
API routes module.
Defines all API endpoints for the application.
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
import httpx
from ..services.wikipedia import WikipediaService
from ..services.outline import OutlineService

router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Wikipedia Country Outline API",
        "version": "1.0.0",
        "endpoints": {
            "/api/outline": "Get Wikipedia outline for a country (query param: ?country=...)",
            "/health": "Health check endpoint"
        },
        "example": "/api/outline?country=India"
    }

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@router.get("/api/outline", response_class=PlainTextResponse)
async def get_country_outline(
    country: str = Query(
        ..., 
        description="Name of the country to fetch Wikipedia outline for",
        example="India"
    )
):
    """
    Get Wikipedia outline for a specified country.
    
    This endpoint fetches the Wikipedia page for the given country,
    extracts all headings (H1-H6), and returns them as a Markdown outline.
    
    Args:
        country: Country name (e.g., "India", "United States", "Vanuatu")
        
    Returns:
        Markdown-formatted outline of the Wikipedia page
        
    Raises:
        HTTPException: If the country is not found or request fails
    """
    try:
        # Validate input
        if not country or not country.strip():
            raise HTTPException(
                status_code=400,
                detail="Country parameter cannot be empty"
            )
        
        # Fetch headings from Wikipedia
        headings = WikipediaService.get_country_headings(country)
        
        if not headings:
            raise HTTPException(
                status_code=404,
                detail=f"No content found for country: {country}"
            )
        
        # Generate markdown outline
        outline = OutlineService.create_outline_with_header(country, headings)
        
        return outline
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Wikipedia page not found for country: {country}"
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error fetching Wikipedia page: {str(e)}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Network error while fetching Wikipedia: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )