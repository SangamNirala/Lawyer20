#!/usr/bin/env python3
"""
🎯 TARGETED LEGAL DOCUMENT EXTRACTION
=====================================
Focused extraction from 5 sources each from Tiers 1-5 
for comprehensive legal document collection demonstration.
"""

import asyncio
import logging
import time
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Core imports
import requests
import aiohttp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

# Configuration imports
from ultra_comprehensive_global_sources import (
    ULTRA_COMPREHENSIVE_GLOBAL_SOURCES,
    get_sources_by_tier,
    SourceConfig,
    SourceType,
    DocumentType
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/backend/targeted_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ExtractionResult:
    """Result of document extraction from a source"""
    source_id: str
    success: bool
    documents_found: int
    documents_extracted: int
    processing_time: float
    error_message: str = None
    sample_documents: List[Dict] = None

class TargetedExtractor:
    """Focused legal document extractor for demonstration"""
    
    def __init__(self):
        self.selected_sources = self._select_demonstration_sources()
        self.extraction_results = []
        self.mongo_client = None
        self.database = None
        
        # Browser setup
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--user-agent=Legal Research Bot 2025')
        self.chrome_options.add_argument('--window-size=1920,1080')
        
        self.chrome_service = Service('/usr/bin/chromedriver')
        
    def _select_demonstration_sources(self) -> Dict[int, List[str]]:
        """Select 5 sources from each of Tiers 1-5 for demonstration"""
        selected = {}
        
        for tier in range(1, 6):  # Tiers 1-5
            tier_sources = get_sources_by_tier(tier)
            
            # Prioritize sources by type and quality
            prioritized_sources = []
            
            for source_id, config in tier_sources.items():
                priority_score = 0
                
                # Prefer API sources (easier extraction)
                if config.source_type == SourceType.API:
                    priority_score += 20
                elif config.source_type == SourceType.RSS_FEED:
                    priority_score += 15
                elif config.source_type == SourceType.WEB_SCRAPING:
                    priority_score += 10
                
                # Add quality score
                priority_score += config.quality_score
                
                # Prefer high-priority sources
                priority_score += (6 - config.priority) * 5
                
                prioritized_sources.append((source_id, priority_score))
            
            # Sort by priority and select top 5
            prioritized_sources.sort(key=lambda x: x[1], reverse=True)
            selected[tier] = [source_id for source_id, _ in prioritized_sources[:5]]
            
            logger.info(f"📊 Tier {tier}: Selected {len(selected[tier])} sources")
            for source_id in selected[tier][:3]:  # Show first 3
                config = tier_sources[source_id]
                logger.info(f"   - {config.name} ({config.source_type.value})")
        
        return selected
    
    async def initialize_database(self):
        """Initialize MongoDB connection"""
        try:
            mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
            self.mongo_client = MongoClient(mongo_url)
            self.database = self.mongo_client['legal_extraction_demo']
            
            # Test connection
            self.mongo_client.server_info()
            logger.info("✅ MongoDB connection initialized")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ MongoDB initialization failed: {e}")
            return False
    
    async def run_targeted_extraction(self):
        """Run the complete targeted extraction process"""
        start_time = time.time()
        
        logger.info("🚀 STARTING TARGETED LEGAL DOCUMENT EXTRACTION")
        logger.info("=" * 60)
        
        # Initialize database
        if not await self.initialize_database():
            return
        
        total_documents = 0
        total_sources = 0
        
        # Process each tier
        for tier in range(1, 6):
            logger.info(f"\n🎯 PROCESSING TIER {tier}")
            logger.info("-" * 40)
            
            tier_sources = self.selected_sources[tier]
            tier_config = get_sources_by_tier(tier)
            
            for source_id in tier_sources:
                if source_id in tier_config:
                    config = tier_config[source_id]
                    result = await self._extract_from_source(source_id, config)
                    self.extraction_results.append(result)
                    
                    total_documents += result.documents_extracted
                    total_sources += 1
                    
                    logger.info(f"{'✅' if result.success else '❌'} {config.name}: "
                               f"{result.documents_extracted} docs in {result.processing_time:.1f}s")
                    
                    # Brief delay between sources
                    await asyncio.sleep(1)
        
        # Generate summary report
        total_time = time.time() - start_time
        await self._generate_extraction_report(total_documents, total_sources, total_time)
    
    async def _extract_from_source(self, source_id: str, config: SourceConfig) -> ExtractionResult:
        """Extract documents from a single source"""
        start_time = time.time()
        
        try:
            logger.info(f"🔄 Processing {config.name} ({config.source_type.value})...")
            
            # Route to appropriate extraction method
            if config.source_type == SourceType.API:
                documents = await self._extract_api_source(source_id, config)
            elif config.source_type == SourceType.RSS_FEED:
                documents = await self._extract_rss_source(source_id, config)
            elif config.source_type == SourceType.WEB_SCRAPING:
                documents = await self._extract_web_source(source_id, config)
            else:
                documents = await self._extract_fallback_source(source_id, config)
            
            # Process and save documents
            processed_docs = await self._process_documents(documents, source_id)
            saved_count = await self._save_documents(processed_docs, source_id)
            
            processing_time = time.time() - start_time
            
            return ExtractionResult(
                source_id=source_id,
                success=True,
                documents_found=len(documents),
                documents_extracted=saved_count,
                processing_time=processing_time,
                sample_documents=processed_docs[:3]  # Keep sample for reporting
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"❌ Error extracting from {source_id}: {e}")
            
            return ExtractionResult(
                source_id=source_id,
                success=False,
                documents_found=0,
                documents_extracted=0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    async def _extract_api_source(self, source_id: str, config: SourceConfig) -> List[Dict]:
        """Extract from API sources"""
        documents = []
        
        try:
            # Use aiohttp for async requests
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                
                if config.api_endpoints:
                    # Process each API endpoint
                    for endpoint_name, endpoint_path in list(config.api_endpoints.items())[:2]:  # Limit to 2 endpoints
                        url = f"{config.base_url.rstrip('/')}/{endpoint_path.lstrip('/')}"
                        
                        try:
                            async with session.get(url) as response:
                                if response.status == 200:
                                    content_type = response.headers.get('content-type', '')
                                    
                                    if 'application/json' in content_type:
                                        data = await response.json()
                                        docs = self._parse_json_response(data, endpoint_name)
                                        documents.extend(docs)
                                    
                                    elif 'text/xml' in content_type or 'application/xml' in content_type:
                                        text = await response.text()
                                        docs = self._parse_xml_response(text, endpoint_name)
                                        documents.extend(docs)
                                    
                                    else:
                                        # Fallback to HTML parsing
                                        text = await response.text()
                                        docs = self._parse_html_response(text, endpoint_name)
                                        documents.extend(docs)
                                        
                        except Exception as e:
                            logger.warning(f"API endpoint {endpoint_name} failed: {e}")
                            continue
                else:
                    # Single API call
                    async with session.get(config.base_url) as response:
                        if response.status == 200:
                            text = await response.text()
                            documents = self._parse_html_response(text, "main")
        
        except Exception as e:
            logger.error(f"API extraction failed for {source_id}: {e}")
        
        return documents[:50]  # Limit to 50 documents per source for demo
    
    async def _extract_rss_source(self, source_id: str, config: SourceConfig) -> List[Dict]:
        """Extract from RSS feed sources"""
        documents = []
        
        try:
            import feedparser
            
            # Parse RSS feed
            feed = feedparser.parse(config.base_url)
            
            for entry in feed.entries[:20]:  # Limit to 20 entries
                doc = {
                    'title': getattr(entry, 'title', 'Untitled'),
                    'content': getattr(entry, 'summary', '') or getattr(entry, 'description', ''),
                    'url': getattr(entry, 'link', ''),
                    'date_published': getattr(entry, 'published', ''),
                    'source_type': 'rss',
                    'author': getattr(entry, 'author', '')
                }
                
                # Clean HTML from content
                if doc['content']:
                    soup = BeautifulSoup(doc['content'], 'html.parser')
                    doc['content'] = soup.get_text(strip=True)
                
                documents.append(doc)
        
        except Exception as e:
            logger.error(f"RSS extraction failed for {source_id}: {e}")
        
        return documents
    
    async def _extract_web_source(self, source_id: str, config: SourceConfig) -> List[Dict]:
        """Extract from web scraping sources"""
        documents = []
        
        try:
            # Use Selenium for JavaScript-heavy sites
            driver = webdriver.Chrome(service=self.chrome_service, options=self.chrome_options)
            
            try:
                driver.get(config.base_url)
                await asyncio.sleep(3)  # Wait for page load
                
                # Look for common legal document patterns
                document_selectors = [
                    'article', '.document', '.case', '.opinion', 
                    '.judgment', '.regulation', '.statute', 
                    '.legal-document', '.content', 'main'
                ]
                
                found_documents = []
                
                for selector in document_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        for element in elements[:10]:  # Limit per selector
                            try:
                                title_elem = element.find_element(By.CSS_SELECTOR, 'h1, h2, h3, .title, .case-title')
                                title = title_elem.text.strip()
                            except:
                                title = "Extracted Legal Document"
                            
                            content = element.text.strip()
                            
                            if len(content) > 200:  # Minimum content length
                                doc = {
                                    'title': title,
                                    'content': content,
                                    'url': driver.current_url,
                                    'extraction_method': f'selenium_{selector}',
                                    'content_length': len(content)
                                }
                                found_documents.append(doc)
                        
                        if found_documents:
                            break  # Found documents with this selector
                    
                    except Exception as e:
                        continue
                
                documents = found_documents
                
            finally:
                driver.quit()
        
        except Exception as e:
            logger.error(f"Web scraping failed for {source_id}: {e}")
        
        return documents[:20]  # Limit to 20 documents
    
    async def _extract_fallback_source(self, source_id: str, config: SourceConfig) -> List[Dict]:
        """Fallback extraction using simple HTTP requests"""
        documents = []
        
        try:
            headers = {
                'User-Agent': 'Legal Research Bot 2025',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            response = requests.get(config.base_url, headers=headers, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                    element.decompose()
                
                # Extract text content
                content = soup.get_text()
                
                # Create a single document from the page
                doc = {
                    'title': soup.title.string if soup.title else "Legal Document",
                    'content': content.strip(),
                    'url': config.base_url,
                    'extraction_method': 'fallback_requests'
                }
                
                if len(doc['content']) > 500:
                    documents.append(doc)
        
        except Exception as e:
            logger.error(f"Fallback extraction failed for {source_id}: {e}")
        
        return documents
    
    def _parse_json_response(self, data: Any, endpoint_name: str) -> List[Dict]:
        """Parse JSON API response to extract documents"""
        documents = []
        
        try:
            if isinstance(data, dict):
                # Look for common JSON structures
                for key in ['results', 'data', 'documents', 'items', 'entries']:
                    if key in data and isinstance(data[key], list):
                        for item in data[key][:20]:  # Limit to 20 items
                            if isinstance(item, dict):
                                doc = self._normalize_document_fields(item)
                                if doc:
                                    documents.append(doc)
                        break
                
                # If no list found, treat whole response as single document
                if not documents and any(field in data for field in ['title', 'content', 'text', 'body']):
                    doc = self._normalize_document_fields(data)
                    if doc:
                        documents.append(doc)
            
            elif isinstance(data, list):
                for item in data[:20]:
                    if isinstance(item, dict):
                        doc = self._normalize_document_fields(item)
                        if doc:
                            documents.append(doc)
        
        except Exception as e:
            logger.error(f"JSON parsing error: {e}")
        
        return documents
    
    def _parse_xml_response(self, xml_text: str, endpoint_name: str) -> List[Dict]:
        """Parse XML API response to extract documents"""
        documents = []
        
        try:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(xml_text)
            
            # Common XML document structures
            doc_elements = (
                root.findall('.//document') or 
                root.findall('.//item') or 
                root.findall('.//entry') or
                root.findall('.//result')
            )
            
            for elem in doc_elements[:20]:  # Limit to 20
                doc = {}
                
                # Extract title
                title_elem = (
                    elem.find('.//title') or 
                    elem.find('.//name') or 
                    elem.find('.//caption')
                )
                if title_elem is not None:
                    doc['title'] = title_elem.text
                
                # Extract content
                content_elem = (
                    elem.find('.//content') or 
                    elem.find('.//text') or 
                    elem.find('.//body') or
                    elem.find('.//description')
                )
                if content_elem is not None:
                    doc['content'] = content_elem.text
                
                # Extract URL
                url_elem = (
                    elem.find('.//url') or 
                    elem.find('.//link') or 
                    elem.find('.//permalink')
                )
                if url_elem is not None:
                    doc['url'] = url_elem.text
                
                if doc.get('title') or doc.get('content'):
                    doc['extraction_method'] = f'xml_{endpoint_name}'
                    documents.append(doc)
        
        except Exception as e:
            logger.error(f"XML parsing error: {e}")
        
        return documents
    
    def _parse_html_response(self, html_text: str, endpoint_name: str) -> List[Dict]:
        """Parse HTML response to extract documents"""
        documents = []
        
        try:
            soup = BeautifulSoup(html_text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Look for document-like structures
            doc_selectors = [
                'article', '.document', '.case', '.opinion', '.judgment',
                '.regulation', '.statute', '.legal-document', '.content-main',
                '.post', '.entry', '.item'
            ]
            
            for selector in doc_selectors:
                elements = soup.select(selector)[:10]  # Limit per selector
                
                for elem in elements:
                    title_elem = elem.select_one('h1, h2, h3, .title, .case-title, .document-title')
                    title = title_elem.get_text(strip=True) if title_elem else "Legal Document"
                    
                    content = elem.get_text(strip=True)
                    
                    if len(content) > 300:  # Minimum content threshold
                        doc = {
                            'title': title,
                            'content': content,
                            'extraction_method': f'html_{endpoint_name}_{selector}',
                            'content_length': len(content)
                        }
                        documents.append(doc)
                
                if documents:
                    break  # Found documents with this selector
        
        except Exception as e:
            logger.error(f"HTML parsing error: {e}")
        
        return documents
    
    def _normalize_document_fields(self, item: Dict) -> Optional[Dict]:
        """Normalize document fields from various data sources"""
        doc = {}
        
        # Extract title from various possible fields
        title_fields = ['title', 'name', 'case_name', 'caption', 'subject', 'headline']
        for field in title_fields:
            if field in item and item[field]:
                doc['title'] = str(item[field]).strip()
                break
        
        # Extract content from various possible fields
        content_fields = ['content', 'text', 'body', 'description', 'summary', 'abstract']
        for field in content_fields:
            if field in item and item[field]:
                content = str(item[field]).strip()
                # Clean HTML if present
                if '<' in content and '>' in content:
                    soup = BeautifulSoup(content, 'html.parser')
                    content = soup.get_text(strip=True)
                doc['content'] = content
                break
        
        # Extract other useful fields
        if 'url' in item or 'link' in item:
            doc['url'] = item.get('url') or item.get('link')
        
        if 'date' in item or 'published' in item or 'created' in item:
            doc['date_published'] = item.get('date') or item.get('published') or item.get('created')
        
        # Only return if we have meaningful content
        if doc.get('title') or (doc.get('content') and len(doc['content']) > 200):
            return doc
        
        return None
    
    async def _process_documents(self, raw_documents: List[Dict], source_id: str) -> List[Dict]:
        """Process and enhance extracted documents"""
        processed = []
        
        for doc in raw_documents:
            try:
                # Basic processing and validation
                processed_doc = {
                    'id': f"{source_id}_{hash(doc.get('title', '') + doc.get('content', '')[:100])}",
                    'title': doc.get('title', 'Untitled Document'),
                    'content': doc.get('content', ''),
                    'source_id': source_id,
                    'source_url': doc.get('url', ''),
                    'extraction_method': doc.get('extraction_method', 'unknown'),
                    'extracted_at': datetime.utcnow(),
                    'content_length': len(doc.get('content', '')),
                    'document_type': self._classify_document_type(doc),
                    'confidence_score': self._calculate_confidence_score(doc)
                }
                
                # Only include documents with sufficient content
                if processed_doc['content_length'] > 200:
                    processed.append(processed_doc)
            
            except Exception as e:
                logger.warning(f"Error processing document: {e}")
                continue
        
        return processed
    
    def _classify_document_type(self, doc: Dict) -> str:
        """Basic document type classification"""
        title = (doc.get('title', '') + ' ' + doc.get('content', '')[:500]).lower()
        
        if any(word in title for word in ['case', 'v.', 'plaintiff', 'defendant', 'court']):
            return 'case_law'
        elif any(word in title for word in ['regulation', 'cfr', 'rule']):
            return 'regulation'
        elif any(word in title for word in ['statute', 'code', 'law', 'act']):
            return 'statute'
        elif any(word in title for word in ['treaty', 'agreement', 'convention']):
            return 'treaty'
        elif any(word in title for word in ['opinion', 'advisory', 'guidance']):
            return 'opinion'
        else:
            return 'administrative'
    
    def _calculate_confidence_score(self, doc: Dict) -> float:
        """Calculate confidence score for extracted document"""
        score = 0.5  # Base score
        
        # Content length bonus
        content_length = len(doc.get('content', ''))
        if content_length > 1000:
            score += 0.2
        elif content_length > 500:
            score += 0.1
        
        # Title bonus
        if doc.get('title') and len(doc['title']) > 10:
            score += 0.1
        
        # URL bonus
        if doc.get('url'):
            score += 0.1
        
        # Legal keywords bonus
        legal_keywords = ['court', 'law', 'legal', 'statute', 'regulation', 'case', 'opinion']
        text = (doc.get('title', '') + ' ' + doc.get('content', '')[:500]).lower()
        keyword_count = sum(1 for keyword in legal_keywords if keyword in text)
        score += min(keyword_count * 0.05, 0.2)
        
        return min(score, 1.0)
    
    async def _save_documents(self, documents: List[Dict], source_id: str) -> int:
        """Save processed documents to MongoDB"""
        if not documents:
            return 0
        
        try:
            collection = self.database[f'documents_{source_id}']
            
            # Insert documents with upsert to avoid duplicates
            saved_count = 0
            for doc in documents:
                try:
                    result = collection.replace_one(
                        {'id': doc['id']}, 
                        doc, 
                        upsert=True
                    )
                    if result.upserted_id or result.modified_count > 0:
                        saved_count += 1
                except Exception as e:
                    logger.warning(f"Error saving document {doc['id']}: {e}")
                    continue
            
            logger.info(f"💾 Saved {saved_count}/{len(documents)} documents for {source_id}")
            return saved_count
            
        except Exception as e:
            logger.error(f"Database save error for {source_id}: {e}")
            return 0
    
    async def _generate_extraction_report(self, total_docs: int, total_sources: int, total_time: float):
        """Generate comprehensive extraction report"""
        logger.info("\n📊 TARGETED EXTRACTION REPORT")
        logger.info("=" * 50)
        
        successful_extractions = [r for r in self.extraction_results if r.success]
        failed_extractions = [r for r in self.extraction_results if not r.success]
        
        logger.info(f"⏱️  Total Processing Time: {total_time:.1f} seconds")
        logger.info(f"📊 Sources Processed: {total_sources}")
        logger.info(f"✅ Successful Extractions: {len(successful_extractions)}")
        logger.info(f"❌ Failed Extractions: {len(failed_extractions)}")
        logger.info(f"📄 Total Documents Extracted: {total_docs}")
        logger.info(f"📈 Average Rate: {total_docs/max(total_time, 1):.1f} docs/second")
        
        # Tier-by-tier breakdown
        logger.info("\n🎯 TIER-BY-TIER BREAKDOWN:")
        for tier in range(1, 6):
            tier_results = [r for r in self.extraction_results 
                           if r.source_id in self.selected_sources[tier]]
            tier_docs = sum(r.documents_extracted for r in tier_results)
            tier_success_rate = len([r for r in tier_results if r.success]) / max(len(tier_results), 1) * 100
            
            logger.info(f"  Tier {tier}: {tier_docs} docs, {tier_success_rate:.1f}% success rate")
        
        # Top performing sources
        logger.info("\n🏆 TOP PERFORMING SOURCES:")
        successful_extractions.sort(key=lambda x: x.documents_extracted, reverse=True)
        for result in successful_extractions[:5]:
            logger.info(f"  {result.source_id}: {result.documents_extracted} docs in {result.processing_time:.1f}s")
        
        # Save detailed report
        report = {
            'extraction_summary': {
                'total_processing_time': total_time,
                'sources_processed': total_sources,
                'successful_extractions': len(successful_extractions),
                'failed_extractions': len(failed_extractions),
                'total_documents': total_docs,
                'documents_per_second': total_docs/max(total_time, 1)
            },
            'detailed_results': [
                {
                    'source_id': r.source_id,
                    'success': r.success,
                    'documents_extracted': r.documents_extracted,
                    'processing_time': r.processing_time,
                    'error_message': r.error_message
                }
                for r in self.extraction_results
            ],
            'selected_sources': self.selected_sources,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        report_file = f'/app/backend/targeted_extraction_report_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"📄 Detailed report saved: {report_file}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("🧹 Database connection closed")

async def main():
    """Main execution function"""
    extractor = TargetedExtractor()
    
    try:
        await extractor.run_targeted_extraction()
    except KeyboardInterrupt:
        logger.info("🛑 Extraction interrupted by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
    finally:
        extractor.cleanup()

if __name__ == "__main__":
    asyncio.run(main())