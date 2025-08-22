#!/usr/bin/env python3
"""
Browser Setup for Legal Document Extraction
===========================================
Sets up headless Chrome for web scraping legal documents with enhanced content extraction
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests
import logging
from typing import Optional, Dict, Any
import asyncio
import aiohttp

# Import enhanced content extractor
from enhanced_content_extractor import IntelligentContentExtractor

logger = logging.getLogger(__name__)

def create_legal_browser():
    """Create optimized Chrome browser for legal document scraping"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Legal document specific optimizations
    chrome_options.add_argument("--disable-images")  # Faster loading
    chrome_options.add_argument("--disable-javascript")  # Many legal sites work without JS
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-extensions")
    
    try:
        # Try to create browser (will fail without proper ChromeDriver)
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logger.warning(f"ChromeDriver not available: {e}")
        return None

async def fetch_with_requests(url: str, headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
    """Fallback method using requests for API sources"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'json' in content_type:
                        data = await response.json()
                    else:
                        data = await response.text()
                    
                    return {
                        'url': url,
                        'status': 'success',
                        'content': data,
                        'content_type': content_type,
                        'status_code': response.status
                    }
                else:
                    return {
                        'url': url,
                        'status': 'error',
                        'error': f'HTTP {response.status}',
                        'status_code': response.status
                    }
    
    except Exception as e:
        return {
            'url': url,
            'status': 'error', 
            'error': str(e)
        }

class DocumentExtractor:
    """Extract documents from legal sources with enhanced content processing"""
    
    def __init__(self):
        self.session = None
        self.content_extractor = IntelligentContentExtractor()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=60),
            headers={
                'User-Agent': 'Legal Research Bot 1.0 (Educational/Research Purpose)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def extract_from_api(self, source_config) -> Dict[str, Any]:
        """Extract documents from API sources"""
        try:
            base_url = source_config.base_url
            api_endpoints = source_config.api_endpoints or {}
            
            documents = []
            
            # Try each API endpoint
            for endpoint_name, endpoint_path in api_endpoints.items():
                full_url = f"{base_url.rstrip('/')}/{endpoint_path.lstrip('/')}"
                
                try:
                    result = await fetch_with_requests(full_url)
                    if result and result['status'] == 'success':
                        # Process the API response
                        content = result['content']
                        
                        # Create mock document for demonstration
                        doc = {
                            'title': f'{source_config.name} - {endpoint_name}',
                            'content': str(content)[:1000] + '...' if len(str(content)) > 1000 else str(content),
                            'url': full_url,
                            'source': source_config.name,
                            'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                            'jurisdiction': source_config.jurisdiction,
                            'extracted_at': '2025-01-18T12:00:00Z'
                        }
                        documents.append(doc)
                        
                except Exception as e:
                    logger.warning(f"API endpoint {endpoint_name} failed: {e}")
            
            return {
                'status': 'success',
                'documents': documents,
                'method': 'api',
                'source_name': source_config.name
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'method': 'api',
                'source_name': source_config.name
            }
    
    async def extract_from_web(self, source_config) -> Dict[str, Any]:
        """Extract documents from web scraping sources"""
        try:
            base_url = source_config.base_url
            
            # Fetch main page
            result = await fetch_with_requests(base_url)
            
            if result and result['status'] == 'success':
                content = result['content']
                
                # Create mock document for demonstration
                doc = {
                    'title': f'{source_config.name} - Main Page',
                    'content': content[:2000] + '...' if len(content) > 2000 else content,
                    'url': base_url,
                    'source': source_config.name,
                    'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                    'jurisdiction': source_config.jurisdiction,
                    'extracted_at': '2025-01-18T12:00:00Z'
                }
                
                return {
                    'status': 'success', 
                    'documents': [doc],
                    'method': 'web_scraping',
                    'source_name': source_config.name
                }
            else:
                return {
                    'status': 'error',
                    'error': result.get('error', 'Unknown error') if result else 'No response',
                    'method': 'web_scraping', 
                    'source_name': source_config.name
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'method': 'web_scraping',
                'source_name': source_config.name
            }

# Test browser setup
if __name__ == "__main__":
    print("🔍 Testing browser setup...")
    
    browser = create_legal_browser()
    if browser:
        print("✅ Chrome browser created successfully")
        browser.quit()
    else:
        print("❌ Chrome browser not available, using fallback methods")
    
    # Test async extraction
    async def test_extraction():
        async with DocumentExtractor() as extractor:
            # Test with a simple source config
            from ultra_comprehensive_global_sources import SourceConfig, SourceType, DocumentType
            
            test_source = SourceConfig(
                name="Test Source",
                source_type=SourceType.WEB_SCRAPING,
                base_url="https://httpbin.org/json",
                estimated_documents=1,
                jurisdiction="Test"
            )
            
            result = await extractor.extract_from_web(test_source)
            print(f"Test result: {result['status']}")
            if result['status'] == 'success':
                print(f"Documents extracted: {len(result['documents'])}")
    
    asyncio.run(test_extraction())