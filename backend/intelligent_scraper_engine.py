"""
Intelligent Legal Document Scraping Engine
AI-Powered with Advanced Error Recovery and Source Adaptation
Optimized for 370M+ documents from 1,000+ sources
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import random
import json
import re
from urllib.parse import urljoin, urlparse
import hashlib
from dataclasses import dataclass
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from bs4 import BeautifulSoup
import feedparser
from fake_useragent import UserAgent

from legal_models import (
    LegalDocument, LegalDocumentCreate, DocumentType, 
    SourceType, ProcessingStatus, PrecedentialValue,
    JurisdictionLevel, LegalSource
)
from legal_sources_config import (
    COMPREHENSIVE_SOURCES, AI_PROCESSING_CONFIG, 
    PERFORMANCE_CONFIG, get_source_config
)

logger = logging.getLogger(__name__)

@dataclass
class ScrapingResult:
    success: bool
    documents: List[Dict[str, Any]]
    errors: List[str]
    source_id: str
    processing_time: float
    documents_found: int
    metadata: Dict[str, Any]

class AIContentProcessor:
    """Advanced AI-powered content processing and extraction"""
    
    def __init__(self):
        self.citation_patterns = {
            'us_case': re.compile(r'\b\d+\s+[A-Za-z\.]+\s+\d+\b'),
            'federal_reporter': re.compile(r'\b\d+\s+F\.\d*d?\s+\d+\b'),
            'supreme_court': re.compile(r'\b\d+\s+U\.S\.\s+\d+\b'),
            'code_section': re.compile(r'\b\d+\s+U\.S\.C\.\s+§\s+\d+\b'),
            'cfr': re.compile(r'\b\d+\s+C\.F\.R\.\s+§\s+\d+\b')
        }
        
        self.legal_topics = {
            'constitutional': ['constitution', 'amendment', 'bill of rights', 'due process'],
            'contract': ['contract', 'agreement', 'breach', 'consideration', 'offer', 'acceptance'],
            'tort': ['negligence', 'liability', 'damages', 'injury', 'duty of care'],
            'criminal': ['criminal', 'prosecution', 'defendant', 'guilty', 'sentence'],
            'corporate': ['corporation', 'shareholder', 'securities', 'merger', 'acquisition'],
            'employment': ['employment', 'discrimination', 'wages', 'workplace', 'harassment'],
            'intellectual_property': ['patent', 'trademark', 'copyright', 'trade secret'],
            'environmental': ['environmental', 'pollution', 'clean air', 'water', 'EPA'],
            'immigration': ['immigration', 'visa', 'deportation', 'asylum', 'citizenship'],
            'tax': ['tax', 'IRS', 'deduction', 'revenue', 'income'],
            'real_estate': ['property', 'real estate', 'landlord', 'tenant', 'mortgage'],
            'family': ['family', 'divorce', 'custody', 'child support', 'adoption'],
            'bankruptcy': ['bankruptcy', 'debt', 'creditor', 'Chapter 7', 'Chapter 11'],
            'antitrust': ['antitrust', 'monopoly', 'competition', 'merger', 'market share']
        }
    
    def extract_citations(self, text: str) -> List[str]:
        """Extract legal citations using AI-enhanced pattern matching"""
        citations = []
        for pattern_name, pattern in self.citation_patterns.items():
            matches = pattern.findall(text)
            citations.extend(matches)
        
        # Remove duplicates and clean up
        return list(set([citation.strip() for citation in citations if citation.strip()]))
    
    def classify_legal_topics(self, text: str) -> List[str]:
        """Classify document into legal topic areas using keyword analysis"""
        text_lower = text.lower()
        topics = []
        
        for topic, keywords in self.legal_topics.items():
            keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
            if keyword_count >= 2:  # Require at least 2 keyword matches
                topics.append(topic)
        
        return topics
    
    def extract_parties(self, text: str, document_type: DocumentType) -> List[str]:
        """Extract party names from legal documents"""
        parties = []
        
        if document_type == DocumentType.CASE_LAW:
            # Pattern for case names like "Smith v. Jones" or "United States v. Defendant"
            case_patterns = [
                re.compile(r'([A-Z][a-zA-Z\s&\.]+)\s+v\.\s+([A-Z][a-zA-Z\s&\.]+)'),
                re.compile(r'([A-Z][a-zA-Z\s&\.]+)\s+vs?\.\s+([A-Z][a-zA-Z\s&\.]+)'),
                re.compile(r'In\s+re:?\s+([A-Z][a-zA-Z\s&\.]+)'),
                re.compile(r'Ex\s+parte:?\s+([A-Z][a-zA-Z\s&\.]+)')
            ]
            
            for pattern in case_patterns:
                matches = pattern.finditer(text)
                for match in matches:
                    parties.extend([group.strip() for group in match.groups() if group.strip()])
        
        return list(set(parties))  # Remove duplicates
    
    def determine_precedential_value(self, court: str, document_type: DocumentType) -> PrecedentialValue:
        """Determine precedential value based on court hierarchy"""
        if not court:
            return PrecedentialValue.INFORMATIONAL
        
        court_lower = court.lower()
        
        if 'supreme court' in court_lower and 'united states' in court_lower:
            return PrecedentialValue.BINDING
        elif 'circuit' in court_lower or 'court of appeals' in court_lower:
            return PrecedentialValue.BINDING
        elif 'district' in court_lower:
            return PrecedentialValue.PERSUASIVE
        elif document_type in [DocumentType.STATUTE, DocumentType.REGULATION]:
            return PrecedentialValue.BINDING
        else:
            return PrecedentialValue.INFORMATIONAL
    
    def calculate_confidence_score(self, document_data: Dict[str, Any]) -> float:
        """Calculate AI confidence score for extracted document"""
        score = 0.0
        factors = 0
        
        # Content completeness (40% weight)
        if document_data.get('title'):
            score += 0.15
        if document_data.get('content') and len(document_data['content']) > 100:
            score += 0.25
        factors += 0.40
        
        # Source reliability (30% weight)
        source_score = document_data.get('source_reliability', 0.8)
        score += source_score * 0.30
        factors += 0.30
        
        # Metadata richness (20% weight)
        metadata_score = 0
        if document_data.get('date_published'):
            metadata_score += 0.05
        if document_data.get('court'):
            metadata_score += 0.05
        if document_data.get('citations'):
            metadata_score += 0.05
        if document_data.get('legal_topics'):
            metadata_score += 0.05
        score += metadata_score
        factors += 0.20
        
        # Citation quality (10% weight)
        citations = document_data.get('citations', [])
        if citations:
            citation_score = min(len(citations) / 10, 1.0) * 0.10
            score += citation_score
        factors += 0.10
        
        return min(score / factors if factors > 0 else 0.5, 1.0)

class IntelligentScrapingEngine:
    """Main scraping engine with AI-powered adaptation and error recovery"""
    
    def __init__(self):
        self.session_pool = {}
        self.driver_pool = {}
        self.ai_processor = AIContentProcessor()
        self.user_agent = UserAgent()
        self.request_history = {}
        self.error_patterns = {}
        self.success_patterns = {}
        
        # Performance tracking
        self.performance_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'sources_processed': set(),
            'documents_extracted': 0
        }
    
    async def initialize_session_pool(self, pool_size: int = 20):
        """Initialize connection pool for API requests"""
        connector = aiohttp.TCPConnector(
            limit=pool_size,
            limit_per_host=5,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': self.user_agent.random}
        )
    
    def create_intelligent_driver(self, headless: bool = True) -> webdriver.Chrome:
        """Create Chrome driver with AI-optimized settings"""
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # Anti-detection measures
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimization
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-css')
        
        # User agent rotation
        options.add_argument(f'--user-agent={self.user_agent.random}')
        
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    async def adaptive_rate_limiting(self, source_id: str):
        """AI-powered adaptive rate limiting based on source behavior"""
        source_config = get_source_config(source_id)
        base_delay = 1.0 / (source_config.get('rate_limit', 100) / 3600)  # Convert hourly to per-request
        
        # Adjust based on recent success rate
        if source_id in self.request_history:
            recent_requests = self.request_history[source_id][-10:]  # Last 10 requests
            if recent_requests:
                success_rate = sum(1 for r in recent_requests if r.get('success')) / len(recent_requests)
                if success_rate < 0.8:  # If success rate below 80%, slow down
                    base_delay *= 2.0
                elif success_rate > 0.95:  # If very successful, can speed up slightly
                    base_delay *= 0.8
        
        # Add jitter to prevent pattern detection
        jitter = random.uniform(0.8, 1.2)
        delay = base_delay * jitter
        
        await asyncio.sleep(delay)
    
    async def scrape_api_source(self, source_id: str, source_config: Dict[str, Any]) -> ScrapingResult:
        """Scrape from API sources with intelligent adaptation"""
        start_time = time.time()
        documents = []
        errors = []
        
        try:
            base_url = source_config['base_url']
            api_endpoints = source_config.get('api_endpoints', {})
            headers = source_config.get('headers', {})
            
            # Merge with default headers
            request_headers = {
                'User-Agent': self.user_agent.random,
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                **headers
            }
            
            for endpoint_name, endpoint_path in api_endpoints.items():
                await self.adaptive_rate_limiting(source_id)
                
                url = urljoin(base_url, endpoint_path)
                
                try:
                    async with self.session.get(url, headers=request_headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            processed_docs = await self.process_api_response(
                                data, source_id, source_config, endpoint_name
                            )
                            documents.extend(processed_docs)
                            
                            # Track success
                            self.track_request_success(source_id, url, True)
                            
                        elif response.status == 429:  # Rate limited
                            retry_after = int(response.headers.get('Retry-After', 60))
                            await asyncio.sleep(retry_after)
                            errors.append(f"Rate limited on {endpoint_name}, waited {retry_after}s")
                        else:
                            error_msg = f"HTTP {response.status} on {endpoint_name}: {url}"
                            errors.append(error_msg)
                            self.track_request_success(source_id, url, False)
                
                except asyncio.TimeoutError:
                    errors.append(f"Timeout on {endpoint_name}: {url}")
                    self.track_request_success(source_id, url, False)
                except Exception as e:
                    errors.append(f"Error on {endpoint_name}: {str(e)}")
                    self.track_request_success(source_id, url, False)
        
        except Exception as e:
            errors.append(f"Fatal error in API scraping: {str(e)}")
        
        processing_time = time.time() - start_time
        
        return ScrapingResult(
            success=len(documents) > 0,
            documents=documents,
            errors=errors,
            source_id=source_id,
            processing_time=processing_time,
            documents_found=len(documents),
            metadata={'endpoint_count': len(api_endpoints)}
        )
    
    async def scrape_web_source(self, source_id: str, source_config: Dict[str, Any]) -> ScrapingResult:
        """Scrape from web sources using intelligent Selenium automation"""
        start_time = time.time()
        documents = []
        errors = []
        driver = None
        
        try:
            driver = self.create_intelligent_driver()
            base_url = source_config['base_url']
            selectors = source_config.get('selectors', {})
            
            # Navigate to base URL
            driver.get(base_url)
            await asyncio.sleep(random.uniform(2, 5))  # Human-like delay
            
            # Find document links
            document_links = await self.find_document_links(driver, source_config)
            
            for link in document_links[:100]:  # Process first 100 documents per session
                await self.adaptive_rate_limiting(source_id)
                
                try:
                    driver.get(link)
                    await asyncio.sleep(random.uniform(1, 3))
                    
                    # Extract document content
                    doc_data = await self.extract_document_content(
                        driver, source_config, link
                    )
                    
                    if doc_data:
                        documents.append(doc_data)
                        self.track_request_success(source_id, link, True)
                    else:
                        errors.append(f"No content extracted from: {link}")
                        self.track_request_success(source_id, link, False)
                
                except Exception as e:
                    errors.append(f"Error processing {link}: {str(e)}")
                    self.track_request_success(source_id, link, False)
        
        except Exception as e:
            errors.append(f"Fatal error in web scraping: {str(e)}")
        
        finally:
            if driver:
                driver.quit()
        
        processing_time = time.time() - start_time
        
        return ScrapingResult(
            success=len(documents) > 0,
            documents=documents,
            errors=errors,
            source_id=source_id,
            processing_time=processing_time,
            documents_found=len(documents),
            metadata={'links_processed': len(document_links) if 'document_links' in locals() else 0}
        )
    
    async def process_api_response(
        self, 
        data: Dict[str, Any], 
        source_id: str, 
        source_config: Dict[str, Any], 
        endpoint_name: str
    ) -> List[Dict[str, Any]]:
        """Process API response data into standardized document format"""
        documents = []
        
        # Handle different response structures
        if isinstance(data, dict):
            if 'results' in data:
                items = data['results']
            elif 'objects' in data:
                items = data['objects']
            elif 'data' in data:
                items = data['data']
            else:
                items = [data]  # Single document
        else:
            items = data if isinstance(data, list) else [data]
        
        for item in items:
            try:
                doc_data = await self.normalize_document_data(item, source_id, source_config)
                if doc_data:
                    documents.append(doc_data)
            except Exception as e:
                logger.error(f"Error processing item from {source_id}: {e}")
        
        return documents
    
    async def normalize_document_data(
        self, 
        raw_data: Dict[str, Any], 
        source_id: str, 
        source_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Normalize raw document data into standard format with AI enhancement"""
        
        # Extract basic fields with intelligent field mapping
        title = self.extract_field_intelligently(raw_data, ['title', 'name', 'case_name', 'caption'])
        content = self.extract_field_intelligently(raw_data, ['content', 'text', 'body', 'html', 'plain_text'])
        date_published = self.extract_date_intelligently(raw_data, ['date_filed', 'date_created', 'date_published', 'created_at'])
        
        if not title and not content:
            return None
        
        # Determine document type
        document_type = self.determine_document_type(raw_data, source_config)
        
        # AI-powered content enhancement
        if content:
            citations = self.ai_processor.extract_citations(content)
            legal_topics = self.ai_processor.classify_legal_topics(content)
            parties = self.ai_processor.extract_parties(content, document_type)
        else:
            citations, legal_topics, parties = [], [], []
        
        # Extract court information
        court = self.extract_field_intelligently(raw_data, ['court', 'court_name', 'issuing_authority'])
        
        # Determine precedential value
        precedential_value = self.ai_processor.determine_precedential_value(court or '', document_type)
        
        # Build normalized document
        doc_data = {
            'title': title or 'Untitled Document',
            'content': content or '',
            'document_type': document_type,
            'jurisdiction': source_config.get('jurisdiction', 'Unknown'),
            'jurisdiction_level': source_config.get('jurisdiction_level', JurisdictionLevel.FEDERAL),
            'court': court,
            'date_published': date_published,
            'citations': citations,
            'legal_topics': legal_topics,
            'parties': parties,
            'precedential_value': precedential_value,
            'source': source_id,
            'source_url': self.extract_field_intelligently(raw_data, ['url', 'absolute_url', 'permalink']),
            'source_reliability': source_config.get('reliability_score', 0.8)
        }
        
        # Calculate AI confidence score
        doc_data['confidence_score'] = self.ai_processor.calculate_confidence_score(doc_data)
        
        return doc_data
    
    def extract_field_intelligently(self, data: Dict[str, Any], field_names: List[str]) -> Optional[str]:
        """Intelligently extract field value from various possible field names"""
        for field_name in field_names:
            value = data.get(field_name)
            if value:
                if isinstance(value, str):
                    return value.strip()
                elif isinstance(value, dict) and 'text' in value:
                    return str(value['text']).strip()
                elif hasattr(value, '__str__'):
                    return str(value).strip()
        return None
    
    def extract_date_intelligently(self, data: Dict[str, Any], field_names: List[str]) -> Optional[datetime]:
        """Intelligently extract and parse date from various formats"""
        for field_name in field_names:
            value = data.get(field_name)
            if value:
                try:
                    if isinstance(value, str):
                        # Try common date formats
                        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
                            try:
                                return datetime.strptime(value[:len(fmt)], fmt)
                            except ValueError:
                                continue
                    elif isinstance(value, datetime):
                        return value
                except Exception:
                    continue
        return None
    
    def determine_document_type(self, data: Dict[str, Any], source_config: Dict[str, Any]) -> DocumentType:
        """Intelligently determine document type based on content and source"""
        # Check source-specific document types
        source_types = source_config.get('document_types', [])
        if len(source_types) == 1:
            return source_types[0]
        
        # Analyze content for type indicators
        content = str(data).lower()
        
        type_indicators = {
            DocumentType.CASE_LAW: ['plaintiff', 'defendant', 'v.', 'court', 'judgment', 'opinion'],
            DocumentType.STATUTE: ['section', 'subsection', 'code', 'act', 'law'],
            DocumentType.REGULATION: ['regulation', 'rule', 'cfr', 'federal register'],
            DocumentType.LEGISLATIVE_BILL: ['bill', 'congress', 'house', 'senate', 'resolution'],
            DocumentType.SCHOLARLY_ARTICLE: ['abstract', 'author', 'university', 'journal', 'doi']
        }
        
        max_score = 0
        best_type = DocumentType.ADMINISTRATIVE
        
        for doc_type, indicators in type_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content)
            if score > max_score:
                max_score = score
                best_type = doc_type
        
        return best_type
    
    def track_request_success(self, source_id: str, url: str, success: bool):
        """Track request success for adaptive optimization"""
        if source_id not in self.request_history:
            self.request_history[source_id] = []
        
        self.request_history[source_id].append({
            'url': url,
            'success': success,
            'timestamp': datetime.utcnow()
        })
        
        # Keep only last 100 requests per source
        if len(self.request_history[source_id]) > 100:
            self.request_history[source_id] = self.request_history[source_id][-100:]
    
    async def find_document_links(self, driver: webdriver.Chrome, source_config: Dict[str, Any]) -> List[str]:
        """Find document links on the page using intelligent selectors"""
        links = []
        
        # Try multiple selector strategies
        selectors = [
            'a[href*="case"]',
            'a[href*="decision"]',
            'a[href*="opinion"]',
            'a[href*="document"]',
            '.case-link a',
            '.document-link a',
            '.judgment-link a'
        ]
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements[:50]:  # Limit to first 50 per selector
                    href = element.get_attribute('href')
                    if href and href not in links:
                        links.append(href)
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
        
        return links
    
    async def extract_document_content(
        self, 
        driver: webdriver.Chrome, 
        source_config: Dict[str, Any], 
        url: str
    ) -> Optional[Dict[str, Any]]:
        """Extract document content using intelligent selectors"""
        selectors = source_config.get('selectors', {})
        
        try:
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract content using configured selectors
            title = self.extract_text_by_selectors(
                driver, selectors.get('case_title', ['h1', 'h2', '.title', '.case-title'])
            )
            
            content = self.extract_text_by_selectors(
                driver, selectors.get('content', ['.content', '.opinion', '.judgment', '.decision'])
            )
            
            court = self.extract_text_by_selectors(
                driver, selectors.get('court_name', ['.court', '.court-name'])
            )
            
            date_text = self.extract_text_by_selectors(
                driver, selectors.get('date', ['.date', '.filed-date', '.decision-date'])
            )
            
            return {
                'title': title,
                'content': content,
                'court': court,
                'date_text': date_text,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def extract_text_by_selectors(self, driver: webdriver.Chrome, selectors: List[str]) -> Optional[str]:
        """Extract text using multiple selector fallbacks"""
        if isinstance(selectors, str):
            selectors = [selectors]
        
        for selector in selectors:
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if text:
                    return text
            except NoSuchElementException:
                continue
        
        return None
    
    async def close(self):
        """Clean up resources"""
        if hasattr(self, 'session'):
            await self.session.close()