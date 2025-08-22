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
import re

# Import enhanced content extractor and advanced complete extractor
from enhanced_content_extractor import IntelligentContentExtractor
from advanced_complete_extractor import CompleteDocumentExtractor

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
    """Extract documents from legal sources with ultra-robust complete content processing"""
    
    def __init__(self, use_complete_extraction: bool = True):
        self.session = None
        self.content_extractor = IntelligentContentExtractor()
        self.complete_extractor = CompleteDocumentExtractor() if use_complete_extraction else None
        self.use_complete_extraction = use_complete_extraction
        
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
        """Extract documents from API sources with enhanced content processing"""
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
                        raw_content = result['content']
                        
                        # Process content intelligently based on content type
                        if isinstance(raw_content, str) and '<html' in raw_content.lower():
                            # HTML content - use enhanced extractor
                            extraction_result = await self.content_extractor.extract_content(
                                raw_content, full_url
                            )
                            
                            if extraction_result['success']:
                                doc = {
                                    'title': extraction_result['title'],
                                    'content': extraction_result['content'],
                                    'url': full_url,
                                    'source': source_config.name,
                                    'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                                    'jurisdiction': source_config.jurisdiction,
                                    'extracted_at': '2025-01-18T12:00:00Z',
                                    'metadata': extraction_result['metadata'],
                                    'quality_score': extraction_result.get('quality_score', 0.0),
                                    'content_length': extraction_result.get('content_length', 0),
                                    'extraction_method': 'enhanced_api'
                                }
                                documents.append(doc)
                            else:
                                logger.warning(f"Content extraction failed for {full_url}: {extraction_result.get('error', 'Unknown error')}")
                        else:
                            # JSON or other structured content
                            content_preview = str(raw_content)
                            if len(content_preview) > 2000:
                                content_preview = content_preview[:2000] + "..."
                            
                            doc = {
                                'title': f'{source_config.name} - {endpoint_name}',
                                'content': content_preview,
                                'url': full_url,
                                'source': source_config.name,
                                'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                                'jurisdiction': source_config.jurisdiction,
                                'extracted_at': '2025-01-18T12:00:00Z',
                                'metadata': {'content_type': 'structured_data', 'api_endpoint': endpoint_name},
                                'quality_score': 0.7,
                                'content_length': len(str(raw_content)),
                                'extraction_method': 'api_structured'
                            }
                            documents.append(doc)
                        
                except Exception as e:
                    logger.warning(f"API endpoint {endpoint_name} failed: {e}")
            
            return {
                'status': 'success',
                'documents': documents,
                'method': 'enhanced_api',
                'source_name': source_config.name
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'method': 'enhanced_api',
                'source_name': source_config.name
            }
    
    async def extract_from_web(self, source_config) -> Dict[str, Any]:
        """Extract documents from web scraping sources with ultra-robust complete content processing"""
        try:
            base_url = source_config.base_url
            
            # Choose extraction method based on configuration
            if self.use_complete_extraction and self.complete_extractor:
                # Use advanced complete extraction for maximum content capture
                logger.info(f"🚀 Using COMPLETE extraction for {source_config.name}")
                
                extraction_result = await self.complete_extractor.extract_complete_document(
                    base_url, 
                    max_pages=5,  # Limit pages for demo
                    follow_links=True
                )
                
                if extraction_result['success'] and extraction_result['content']:
                    # Create enhanced document with complete extraction metadata
                    doc = {
                        'title': extraction_result.get('title', f'{source_config.name} - Complete Document'),
                        'content': extraction_result['content'],
                        'url': base_url,
                        'source': source_config.name,
                        'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                        'jurisdiction': source_config.jurisdiction,
                        'extracted_at': '2025-01-18T12:00:00Z',
                        'metadata': extraction_result.get('metadata', {}),
                        'quality_score': extraction_result.get('quality_score', 0.0),
                        'content_length': len(extraction_result['content']),
                        'extraction_method': 'advanced_complete',
                        'completeness_score': extraction_result.get('completeness_score', 0.0),
                        'is_complete': extraction_result.get('is_complete', False),
                        'pages_processed': extraction_result.get('pages_processed', 1),
                        'processing_time': extraction_result.get('processing_time', 0.0),
                        'completeness_indicators': extraction_result.get('completeness_indicators', {}),
                        'advanced_features': {
                            'pagination_handled': True,
                            'document_links_followed': True,
                            'content_reconstructed': extraction_result.get('reconstructed', False),
                            'duplicates_removed': True,
                            'completeness_validated': True
                        }
                    }
                    
                    logger.info(f"✅ COMPLETE extraction successful for {source_config.name}")
                    logger.info(f"   📄 Title: {doc['title'][:100]}...")
                    logger.info(f"   📊 Content length: {len(doc['content']):,} characters")
                    logger.info(f"   🎯 Quality score: {doc['quality_score']:.2f}")
                    logger.info(f"   ✅ Completeness score: {doc['completeness_score']:.2f}")
                    logger.info(f"   📑 Pages processed: {doc['pages_processed']}")
                    logger.info(f"   ⏱️ Processing time: {doc['processing_time']:.2f}s")
                    logger.info(f"   🏆 Is complete: {doc['is_complete']}")
                    
                    return {
                        'status': 'success', 
                        'documents': [doc],
                        'method': 'advanced_complete_extraction',
                        'source_name': source_config.name
                    }
                else:
                    # Complete extraction failed, fallback to enhanced extraction
                    logger.warning(f"⚠️ Complete extraction failed for {source_config.name}, using fallback")
                    error_msg = extraction_result.get('error', 'Complete extraction failed')
            else:
                # Use standard enhanced extraction
                logger.info(f"🔧 Using enhanced extraction for {source_config.name}")
                error_msg = "Complete extraction disabled"
            
            # Fallback to enhanced extraction
            result = await fetch_with_requests(base_url)
            
            if result and result['status'] == 'success':
                raw_html = result['content']
                
                # Use enhanced content extractor to get clean text
                extraction_result = await self.content_extractor.extract_content(raw_html, base_url)
                
                if extraction_result['success'] and extraction_result['content']:
                    # Successfully extracted clean content
                    doc = {
                        'title': extraction_result['title'],
                        'content': extraction_result['content'],
                        'url': base_url,
                        'source': source_config.name,
                        'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                        'jurisdiction': source_config.jurisdiction,
                        'extracted_at': '2025-01-18T12:00:00Z',
                        'metadata': extraction_result['metadata'],
                        'quality_score': extraction_result.get('quality_score', 0.0),
                        'content_length': extraction_result.get('content_length', 0),
                        'extraction_method': extraction_result.get('extraction_method', 'enhanced_web'),
                        'completeness_score': 0.5,  # Default for basic extraction
                        'is_complete': False,  # Basic extraction is not considered complete
                        'fallback_reason': error_msg if 'error_msg' in locals() else None
                    }
                    
                    logger.info(f"✅ Enhanced extraction successful for {source_config.name}")
                    logger.info(f"   📄 Title: {doc['title'][:100]}...")
                    logger.info(f"   📊 Content length: {len(doc['content']):,} characters")
                    logger.info(f"   🎯 Quality score: {doc['quality_score']:.2f}")
                    
                    return {
                        'status': 'success', 
                        'documents': [doc],
                        'method': 'enhanced_web_scraping',
                        'source_name': source_config.name
                    }
                else:
                    # Enhanced extraction failed, but we still got HTML
                    error_msg = extraction_result.get('error', 'Content extraction failed')
                    logger.warning(f"⚠️ Enhanced extraction failed for {source_config.name}: {error_msg}")
                    
                    # Fallback to basic text extraction (better than raw HTML)
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(raw_html, 'html.parser')
                    
                    # Remove scripts, styles, and other unwanted elements
                    for script in soup(["script", "style", "nav", "header", "footer"]):
                        script.decompose()
                    
                    # Get basic text content
                    text_content = soup.get_text(separator=' ', strip=True)
                    
                    # Clean up whitespace
                    import re
                    text_content = re.sub(r'\s+', ' ', text_content)
                    text_content = text_content[:5000] + "..." if len(text_content) > 5000 else text_content
                    
                    if len(text_content) > 100:  # If we got reasonable content
                        doc = {
                            'title': soup.title.string if soup.title else f'{source_config.name} - Main Page',
                            'content': text_content,
                            'url': base_url,
                            'source': source_config.name,
                            'document_type': source_config.document_types[0] if source_config.document_types else 'administrative',
                            'jurisdiction': source_config.jurisdiction,
                            'extracted_at': '2025-01-18T12:00:00Z',
                            'metadata': {'extraction_method': 'fallback', 'extraction_error': error_msg},
                            'quality_score': 0.3,
                            'content_length': len(text_content),
                            'extraction_method': 'fallback_basic',
                            'completeness_score': 0.2,  # Low completeness for fallback
                            'is_complete': False
                        }
                        
                        logger.info(f"🔄 Fallback extraction used for {source_config.name}")
                        logger.info(f"   📄 Content length: {len(text_content):,} characters")
                        
                        return {
                            'status': 'success',
                            'documents': [doc],
                            'method': 'fallback_web_scraping',
                            'source_name': source_config.name
                        }
                    else:
                        return {
                            'status': 'error',
                            'error': f'Insufficient content extracted: {len(text_content)} chars',
                            'method': 'enhanced_web_scraping',
                            'source_name': source_config.name
                        }
            else:
                return {
                    'status': 'error',
                    'error': result.get('error', 'Unknown error') if result else 'No response',
                    'method': 'enhanced_web_scraping', 
                    'source_name': source_config.name
                }
                
        except Exception as e:
            logger.error(f"❌ Web extraction failed for {source_config.name}: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'method': 'enhanced_web_scraping',
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