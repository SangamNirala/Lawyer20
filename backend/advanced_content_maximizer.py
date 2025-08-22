#!/usr/bin/env python3
"""
🚀 ADVANCED CONTENT MAXIMIZER SYSTEM
====================================
Advanced system for maximizing legal content extraction through legitimate channels:
1. API Key Management & Official Access
2. Academic/Research Institution Access
3. Public Data Repository Integration
4. Advanced Free Content Enhancement
5. Legal Content Aggregator Networks
6. Alternative Source Discovery
7. Content Reconstruction from Multiple Sources
8. Enhanced Metadata Extraction
"""

import asyncio
import logging
import time
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
import re
from urllib.parse import urljoin, urlparse
import hashlib

# Enhanced imports
import aiohttp
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import feedparser
import pymongo

# Set up enhanced logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContentSource:
    """Enhanced content source with multiple access methods"""
    source_id: str
    name: str
    base_url: str
    api_endpoints: Dict[str, str] = field(default_factory=dict)
    rss_feeds: List[str] = field(default_factory=list)
    sitemap_urls: List[str] = field(default_factory=list)
    alternative_sources: List[str] = field(default_factory=list)
    public_repositories: List[str] = field(default_factory=list)
    archive_urls: List[str] = field(default_factory=list)
    requires_auth: bool = False
    estimated_free_content: int = 0

@dataclass
class ExtractionResult:
    """Comprehensive extraction result"""
    source_id: str
    total_documents: int
    high_quality_docs: int
    partial_docs: int
    methods_used: List[str]
    processing_time: float
    content_sources: Dict[str, int]
    success_rate: float

class AdvancedContentMaximizer:
    """
    Advanced system for maximizing legal content extraction
    Uses multiple legitimate strategies to access maximum content
    """
    
    def __init__(self):
        self.content_sources = self._initialize_enhanced_sources()
        self.api_keys = self._load_api_keys()
        self.session_manager = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Academic-Legal-Research-Bot/2.0 (Educational Purpose)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
        )
        
        # Advanced browser setup
        self.browser_options = self._setup_enhanced_browser()
        self.chrome_service = Service('/usr/bin/chromedriver')
        
        # Content deduplication
        self.content_hashes: Set[str] = set()
        
        # MongoDB for advanced storage
        self.mongo_client = None
        self.database = None
        
    def _initialize_enhanced_sources(self) -> Dict[str, ContentSource]:
        """Initialize enhanced source configurations with multiple access points"""
        
        return {
            "texas_bar_enhanced": ContentSource(
                source_id="texas_bar_enhanced",
                name="Texas State Bar - Enhanced Access",
                base_url="https://www.texasbar.com",
                rss_feeds=[
                    "https://www.texasbar.com/RSS.aspx",
                    "https://www.texasbar.com/Content/NavigationMenu/NewsandPublications/TexasBarJournal/RSS_TBJ.xml"
                ],
                sitemap_urls=[
                    "https://www.texasbar.com/sitemap.xml"
                ],
                alternative_sources=[
                    "https://www.americanbar.org/groups/state_local_bar/resources/state-bar-websites/texas/",
                    "https://www.law360.com/texas",
                    "https://www.reuters.com/legal/legalindustry/",
                    "https://news.bloomberglaw.com/",
                    "https://www.law.com/texaslawyer/",
                    "https://legalnews.com/texas"
                ],
                public_repositories=[
                    "https://scholar.google.com/scholar?q=site:texasbar.com",
                    "https://web.archive.org/web/*/texasbar.com/*",
                    "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_page=25&txtSearch=texas+bar"
                ],
                estimated_free_content=500
            ),
            
            "harvard_law_enhanced": ContentSource(
                source_id="harvard_law_enhanced", 
                name="Harvard Law School - Enhanced Access",
                base_url="https://hls.harvard.edu",
                api_endpoints={
                    "digital_collections": "/library/digital-collections",
                    "faculty_research": "/faculty/research",
                    "library_catalog": "/library/catalog"
                },
                rss_feeds=[
                    "https://hls.harvard.edu/news/feed/",
                    "https://blogs.harvard.edu/law/feed/"
                ],
                alternative_sources=[
                    "https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_page=25&txtSearch=harvard+law",
                    "https://scholar.google.com/scholar?q=site:harvard.edu+law",
                    "https://digitalcommons.law.harvard.edu/",
                    "https://dash.harvard.edu/browse?type=subject&value=Law",
                    "https://cyber.harvard.edu/publications",
                    "https://clinics.law.harvard.edu/",
                    "https://harvardlawreview.org/",
                    "https://www.repository.law.indiana.edu/cgi/search.cgi?q=harvard"
                ],
                public_repositories=[
                    "https://dash.harvard.edu/",
                    "https://nrs.harvard.edu/",
                    "https://www.repository.law.indiana.edu/",
                    "https://digitalcommons.law.yale.edu/",
                    "https://scholarship.law.columbia.edu/"
                ],
                estimated_free_content=2000
            ),
            
            "law360_enhanced": ContentSource(
                source_id="law360_enhanced",
                name="Law360 - Enhanced Access",
                base_url="https://www.law360.com",
                rss_feeds=[
                    "https://www.law360.com/rss/sections/all",
                    "https://www.law360.com/rss/articles/latest"
                ],
                alternative_sources=[
                    "https://www.reuters.com/legal/",
                    "https://news.bloomberglaw.com/",
                    "https://www.americanlawyer.com/",
                    "https://www.law.com/",
                    "https://www.lexisnexis.com/community/insights/",
                    "https://www.thomsonreuters.com/en/press-releases/legal.html",
                    "https://www.jdsupra.com/",
                    "https://www.lawsitesblog.com/"
                ],
                public_repositories=[
                    "https://scholar.google.com/scholar?q=law360",
                    "https://web.archive.org/web/*/law360.com/*"
                ],
                estimated_free_content=1000
            )
        }
    
    def _setup_enhanced_browser(self) -> Options:
        """Setup enhanced browser with advanced capabilities"""
        options = Options()
        
        # Core options
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Advanced content access options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Performance optimizations
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')  # For basic content extraction
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-extensions')
        
        # Stealth options
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Academic-Research-Bot/1.0')
        options.add_argument('--accept-lang=en-US,en;q=0.9')
        
        return options
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load available API keys for official access"""
        api_keys = {}
        
        # Check for environment variables
        potential_keys = [
            'WESTLAW_API_KEY', 'LEXISNEXIS_API_KEY', 'COURTLISTENER_API_KEY',
            'HARVARD_LIBRARY_API_KEY', 'SSRN_API_KEY', 'GOOGLE_SCHOLAR_API_KEY'
        ]
        
        for key_name in potential_keys:
            if key_name in os.environ:
                api_keys[key_name.lower()] = os.environ[key_name]
                logger.info(f"✅ Found API key: {key_name}")
        
        return api_keys
    
    async def maximize_content_extraction(self, source_ids: List[str]) -> Dict[str, Any]:
        """
        Main method to maximize content extraction using all legitimate methods
        """
        logger.info("🚀 STARTING ADVANCED CONTENT MAXIMIZER")
        logger.info("=" * 70)
        
        # Initialize database
        await self._initialize_database()
        
        extraction_summary = {
            "total_sources": len(source_ids),
            "total_documents_extracted": 0,
            "high_quality_documents": 0,
            "method_performance": {},
            "source_results": {},
            "alternative_sources_discovered": 0,
            "processing_time": 0
        }
        
        start_time = time.time()
        
        for source_id in source_ids:
            if source_id in self.content_sources:
                logger.info(f"\n🎯 PROCESSING: {self.content_sources[source_id].name}")
                logger.info("-" * 50)
                
                result = await self._extract_from_enhanced_source(source_id)
                extraction_summary["source_results"][source_id] = result
                extraction_summary["total_documents_extracted"] += result.total_documents
                extraction_summary["high_quality_documents"] += result.high_quality_docs
                
                # Update method performance tracking
                for method in result.methods_used:
                    if method not in extraction_summary["method_performance"]:
                        extraction_summary["method_performance"][method] = {"success": 0, "total": 0}
                    extraction_summary["method_performance"][method]["total"] += 1
                    if result.success_rate > 0.5:
                        extraction_summary["method_performance"][method]["success"] += 1
        
        extraction_summary["processing_time"] = time.time() - start_time
        
        # Generate comprehensive report
        await self._generate_maximization_report(extraction_summary)
        
        return extraction_summary
    
    async def _extract_from_enhanced_source(self, source_id: str) -> ExtractionResult:
        """Extract content from source using all available methods"""
        
        source = self.content_sources[source_id]
        all_documents = []
        methods_used = []
        content_sources = {}
        
        start_time = time.time()
        
        # Method 1: RSS Feed Extraction
        if source.rss_feeds:
            logger.info("📡 Extracting from RSS feeds...")
            rss_docs = await self._extract_from_rss_feeds(source)
            all_documents.extend(rss_docs)
            if rss_docs:
                methods_used.append("rss_feeds")
                content_sources["rss_feeds"] = len(rss_docs)
        
        # Method 2: Enhanced Web Scraping with Multiple Strategies
        logger.info("🌐 Enhanced web scraping...")
        web_docs = await self._enhanced_web_scraping(source)
        all_documents.extend(web_docs)
        if web_docs:
            methods_used.append("enhanced_web_scraping")
            content_sources["web_scraping"] = len(web_docs)
        
        # Method 3: Alternative Source Extraction
        logger.info("🔄 Extracting from alternative sources...")
        alt_docs = await self._extract_from_alternatives(source)
        all_documents.extend(alt_docs)
        if alt_docs:
            methods_used.append("alternative_sources")
            content_sources["alternative_sources"] = len(alt_docs)
        
        # Method 4: Public Repository Mining
        logger.info("📚 Mining public repositories...")
        repo_docs = await self._extract_from_repositories(source)
        all_documents.extend(repo_docs)
        if repo_docs:
            methods_used.append("public_repositories")
            content_sources["public_repositories"] = len(repo_docs)
        
        # Method 5: Archive.org and Historical Content
        logger.info("🏛️ Accessing archived content...")
        archive_docs = await self._extract_from_archives(source)
        all_documents.extend(archive_docs)
        if archive_docs:
            methods_used.append("archive_access")
            content_sources["archive_access"] = len(archive_docs)
        
        # Method 6: Content Reconstruction from Fragments
        logger.info("🔧 Reconstructing content from fragments...")
        reconstructed_docs = await self._reconstruct_content_fragments(all_documents)
        all_documents.extend(reconstructed_docs)
        if reconstructed_docs:
            methods_used.append("content_reconstruction")
            content_sources["content_reconstruction"] = len(reconstructed_docs)
        
        # Deduplicate and quality filter
        unique_documents = await self._deduplicate_and_filter(all_documents)
        high_quality_docs = [doc for doc in unique_documents if doc.get('content_length', 0) > 500]
        
        # Save to database
        await self._save_enhanced_documents(unique_documents, source_id)
        
        processing_time = time.time() - start_time
        
        return ExtractionResult(
            source_id=source_id,
            total_documents=len(unique_documents),
            high_quality_docs=len(high_quality_docs),
            partial_docs=len(unique_documents) - len(high_quality_docs),
            methods_used=methods_used,
            processing_time=processing_time,
            content_sources=content_sources,
            success_rate=len(unique_documents) / max(source.estimated_free_content, 1)
        )
    
    async def _extract_from_rss_feeds(self, source: ContentSource) -> List[Dict[str, Any]]:
        """Extract content from RSS feeds with enhanced parsing"""
        documents = []
        
        for feed_url in source.rss_feeds:
            try:
                logger.info(f"   📡 Processing feed: {feed_url}")
                
                # Parse RSS feed
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:50]:  # Limit per feed
                    try:
                        # Extract comprehensive content from RSS entry
                        content = self._extract_rss_content(entry)
                        
                        if len(content) > 100:  # Minimum content threshold
                            doc = {
                                "title": entry.get('title', 'RSS Article'),
                                "content": content,
                                "url": entry.get('link', feed_url),
                                "published_date": entry.get('published', ''),
                                "author": entry.get('author', ''),
                                "source_id": source.source_id,
                                "extraction_method": "rss_feed",
                                "content_length": len(content),
                                "feed_source": feed_url,
                                "extracted_at": datetime.utcnow().isoformat()
                            }
                            documents.append(doc)
                    
                    except Exception as e:
                        continue
                
                logger.info(f"   ✅ Extracted {len([d for d in documents if d.get('feed_source') == feed_url])} documents from RSS feed")
            
            except Exception as e:
                logger.warning(f"   ❌ RSS feed failed {feed_url}: {e}")
                continue
        
        return documents
    
    async def _enhanced_web_scraping(self, source: ContentSource) -> List[Dict[str, Any]]:
        """Enhanced web scraping with multiple content discovery strategies"""
        documents = []
        
        try:
            driver = webdriver.Chrome(service=self.chrome_service, options=self.browser_options)
            
            try:
                # Load main page
                driver.get(source.base_url)
                await asyncio.sleep(3)
                
                # Strategy 1: Article/News Discovery
                articles = await self._discover_articles(driver, source)
                documents.extend(articles)
                
                # Strategy 2: Publication/Document Discovery  
                publications = await self._discover_publications(driver, source)
                documents.extend(publications)
                
                # Strategy 3: News/Press Release Discovery
                news_items = await self._discover_news_items(driver, source)
                documents.extend(news_items)
                
                # Strategy 4: Deep Link Discovery
                deep_links = await self._discover_deep_content(driver, source)
                documents.extend(deep_links)
                
                logger.info(f"   ✅ Enhanced web scraping extracted {len(documents)} documents")
            
            finally:
                driver.quit()
        
        except Exception as e:
            logger.error(f"Enhanced web scraping failed: {e}")
        
        return documents
    
    async def _extract_from_alternatives(self, source: ContentSource) -> List[Dict[str, Any]]:
        """Extract content from alternative sources"""
        documents = []
        
        for alt_url in source.alternative_sources[:5]:  # Limit to top 5 alternatives
            try:
                logger.info(f"   🔄 Processing alternative: {alt_url}")
                
                async with self.session_manager.get(alt_url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        soup = BeautifulSoup(html_content, 'html.parser')
                        
                        # Extract relevant content related to original source
                        relevant_content = await self._extract_relevant_content(soup, source, alt_url)
                        documents.extend(relevant_content)
                        
                        if relevant_content:
                            logger.info(f"   ✅ Found {len(relevant_content)} relevant documents")
            
            except Exception as e:
                logger.warning(f"   ❌ Alternative source failed {alt_url}: {e}")
                continue
        
        return documents
    
    async def _extract_from_repositories(self, source: ContentSource) -> List[Dict[str, Any]]:
        """Extract content from public repositories"""
        documents = []
        
        for repo_url in source.public_repositories:
            try:
                logger.info(f"   📚 Processing repository: {repo_url}")
                
                if "scholar.google.com" in repo_url:
                    # Google Scholar extraction
                    scholar_docs = await self._extract_from_google_scholar(repo_url, source)
                    documents.extend(scholar_docs)
                
                elif "ssrn.com" in repo_url:
                    # SSRN extraction
                    ssrn_docs = await self._extract_from_ssrn(repo_url, source)
                    documents.extend(ssrn_docs)
                    
                elif "archive.org" in repo_url:
                    # Archive.org extraction
                    archive_docs = await self._extract_from_wayback(repo_url, source)
                    documents.extend(archive_docs)
                
                else:
                    # Generic repository extraction
                    generic_docs = await self._extract_from_generic_repo(repo_url, source)
                    documents.extend(generic_docs)
                
                if documents:
                    logger.info(f"   ✅ Repository extraction found {len([d for d in documents if repo_url in d.get('source_url', '')])} documents")
            
            except Exception as e:
                logger.warning(f"   ❌ Repository failed {repo_url}: {e}")
                continue
        
        return documents
    
    async def _extract_from_archives(self, source: ContentSource) -> List[Dict[str, Any]]:
        """Extract content from web archives"""
        documents = []
        
        try:
            # Wayback Machine API
            wayback_api = f"http://archive.org/wayback/available?url={source.base_url}"
            
            async with self.session_manager.get(wayback_api) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                        archive_url = data['archived_snapshots']['closest']['url']
                        timestamp = data['archived_snapshots']['closest']['timestamp']
                        
                        # Extract content from archived version
                        archive_docs = await self._extract_from_archived_page(archive_url, timestamp, source)
                        documents.extend(archive_docs)
                        
                        logger.info(f"   ✅ Archive extraction found {len(archive_docs)} documents")
        
        except Exception as e:
            logger.warning(f"Archive extraction failed: {e}")
        
        return documents
    
    async def _reconstruct_content_fragments(self, existing_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reconstruct full content from multiple partial documents"""
        reconstructed = []
        
        # Group documents by similarity
        doc_groups = self._group_similar_documents(existing_docs)
        
        for group in doc_groups:
            if len(group) > 1:  # Only reconstruct if we have multiple fragments
                try:
                    reconstructed_doc = self._merge_document_fragments(group)
                    if reconstructed_doc and reconstructed_doc.get('content_length', 0) > 1000:
                        reconstructed.append(reconstructed_doc)
                except Exception as e:
                    continue
        
        if reconstructed:
            logger.info(f"   🔧 Reconstructed {len(reconstructed)} documents from fragments")
        
        return reconstructed
    
    async def _deduplicate_and_filter(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and filter low-quality content"""
        unique_docs = []
        seen_hashes = set()
        
        for doc in documents:
            # Create content hash for deduplication
            content_hash = hashlib.md5(doc.get('content', '').encode()).hexdigest()
            
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                
                # Quality filtering
                if self._passes_quality_filter(doc):
                    unique_docs.append(doc)
        
        logger.info(f"   🔍 After deduplication and filtering: {len(unique_docs)} unique documents")
        return unique_docs
    
    def _passes_quality_filter(self, doc: Dict[str, Any]) -> bool:
        """Check if document passes quality filters"""
        content = doc.get('content', '')
        
        # Minimum length
        if len(content) < 100:
            return False
        
        # Legal content indicators
        legal_keywords = ['law', 'legal', 'court', 'case', 'statute', 'regulation', 'attorney', 'justice']
        if not any(keyword in content.lower() for keyword in legal_keywords):
            return False
        
        # Not just navigation/boilerplate
        if any(phrase in content.lower() for phrase in ['cookie policy', 'privacy policy', 'subscribe now']):
            return False
        
        return True
    
    async def _save_enhanced_documents(self, documents: List[Dict[str, Any]], source_id: str):
        """Save documents to enhanced database structure"""
        if not documents:
            return
        
        try:
            collection = self.database[f'enhanced_{source_id}']
            
            saved_count = 0
            for doc in documents:
                try:
                    # Add enhanced metadata
                    doc['extraction_enhanced'] = True
                    doc['extraction_timestamp'] = datetime.utcnow()
                    doc['quality_score'] = self._calculate_quality_score(doc)
                    
                    result = collection.replace_one(
                        {'content_hash': hashlib.md5(doc.get('content', '').encode()).hexdigest()},
                        doc,
                        upsert=True
                    )
                    
                    if result.upserted_id or result.modified_count > 0:
                        saved_count += 1
                
                except Exception as e:
                    continue
            
            logger.info(f"   💾 Saved {saved_count} enhanced documents to database")
        
        except Exception as e:
            logger.error(f"Database save failed: {e}")

    # Helper methods (placeholders for complex implementations)
    def _extract_rss_content(self, entry) -> str:
        """Extract enhanced content from RSS entry"""
        content_parts = []
        
        # Try multiple content fields
        for field in ['content', 'description', 'summary']:
            if hasattr(entry, field):
                field_content = getattr(entry, field)
                if isinstance(field_content, list) and field_content:
                    content_parts.append(field_content[0].get('value', ''))
                elif isinstance(field_content, str):
                    content_parts.append(field_content)
        
        # Clean and combine
        full_content = ' '.join(content_parts)
        soup = BeautifulSoup(full_content, 'html.parser')
        return soup.get_text(strip=True)
    
    async def _discover_articles(self, driver, source: ContentSource) -> List[Dict[str, Any]]:
        """Discover article content using advanced selectors"""
        articles = []
        
        article_selectors = [
            'article', '.article', '.post', '.news-item', '.blog-post',
            '.content-item', '.publication', '.document-preview'
        ]
        
        for selector in article_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements[:10]:  # Limit per selector
                    article_data = self._extract_article_data(element, driver.current_url)
                    if article_data:
                        articles.append(article_data)
            except:
                continue
        
        return articles
    
    def _extract_article_data(self, element, base_url: str) -> Optional[Dict[str, Any]]:
        """Extract comprehensive article data from element"""
        try:
            # Extract title
            title_elem = element.find_element(By.CSS_SELECTOR, 'h1, h2, h3, .title, .headline')
            title = title_elem.text.strip()
            
            # Extract content
            content = element.text.strip()
            
            # Extract link if available
            try:
                link_elem = element.find_element(By.CSS_SELECTOR, 'a[href]')
                link = link_elem.get_attribute('href')
                if not link.startswith('http'):
                    link = urljoin(base_url, link)
            except:
                link = base_url
            
            if len(content) > 200:  # Minimum threshold
                return {
                    "title": title,
                    "content": content,
                    "url": link,
                    "extraction_method": "article_discovery",
                    "content_length": len(content),
                    "extracted_at": datetime.utcnow().isoformat()
                }
        
        except:
            pass
        
        return None
    
    async def _initialize_database(self):
        """Initialize enhanced database connection"""
        try:
            mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
            self.mongo_client = pymongo.MongoClient(mongo_url)
            self.database = self.mongo_client['enhanced_legal_extraction']
            
            # Test connection
            self.mongo_client.server_info()
            logger.info("✅ Enhanced database connection initialized")
        
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
    
    # Placeholder methods for complex implementations
    async def _discover_publications(self, driver, source): return []
    async def _discover_news_items(self, driver, source): return []
    async def _discover_deep_content(self, driver, source): return []
    async def _extract_relevant_content(self, soup, source, url): return []
    async def _extract_from_google_scholar(self, url, source): return []
    async def _extract_from_ssrn(self, url, source): return []
    async def _extract_from_wayback(self, url, source): return []
    async def _extract_from_generic_repo(self, url, source): return []
    async def _extract_from_archived_page(self, url, timestamp, source): return []
    
    def _group_similar_documents(self, docs): return []
    def _merge_document_fragments(self, group): return None
    def _calculate_quality_score(self, doc): return 0.8
    
    async def _generate_maximization_report(self, summary):
        """Generate comprehensive maximization report"""
        report_file = f'/app/backend/content_maximization_report_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"📄 Maximization report saved: {report_file}")

# Test the system
async def main():
    """Test the advanced content maximizer"""
    maximizer = AdvancedContentMaximizer()
    
    test_sources = ["texas_bar_enhanced", "harvard_law_enhanced", "law360_enhanced"]
    
    results = await maximizer.maximize_content_extraction(test_sources)
    
    logger.info("\n🎯 CONTENT MAXIMIZATION RESULTS:")
    logger.info(f"Total Documents Extracted: {results['total_documents_extracted']}")
    logger.info(f"High Quality Documents: {results['high_quality_documents']}")
    logger.info(f"Processing Time: {results['processing_time']:.1f} seconds")

if __name__ == "__main__":
    asyncio.run(main())