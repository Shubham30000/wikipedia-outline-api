"""
Caching utility module.
Implements file-based caching to avoid redundant HTTP requests.
"""
import hashlib
from pathlib import Path
from typing import Optional
import httpx
from .config import settings

def cached_get(url: str) -> str:
    """
    Fetch a URL with file-based caching.
    
    If the URL has been fetched before, return the cached content.
    Otherwise, fetch the URL, cache the response, and return it.
    
    Args:
        url: The URL to fetch
        
    Returns:
        The HTML content as a string
        
    Raises:
        httpx.HTTPError: If the request fails
    """
    # Generate a unique filename based on URL hash
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_path = settings.CACHE_DIR / filename
    
    # Check if cached version exists
    if cache_path.exists():
        print(f"[CACHE HIT] Loading from cache: {url}")
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    # Fetch from web
    print(f"[CACHE MISS] Fetching from web: {url}")
    response = httpx.get(
        url,
        timeout=settings.REQUEST_TIMEOUT,
        headers={'User-Agent': settings.USER_AGENT},
        follow_redirects=True
    )
    response.raise_for_status()
    
    # Save to cache
    with open(cache_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    return response.text

def clear_cache(url: Optional[str] = None) -> None:
    """
    Clear cached content.
    
    Args:
        url: If provided, clear only this URL's cache. Otherwise, clear all.
    """
    if url:
        filename = hashlib.md5(url.encode('utf-8')).hexdigest()
        cache_path = settings.CACHE_DIR / filename
        if cache_path.exists():
            cache_path.unlink()
            print(f"[CACHE] Cleared cache for: {url}")
    else:
        for cache_file in settings.CACHE_DIR.glob("*"):
            if cache_file.is_file():
                cache_file.unlink()
        print("[CACHE] Cleared all cache files")