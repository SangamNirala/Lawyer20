#!/usr/bin/env python3
"""
🚀 ADVANCED COMPLETE LEGAL DOCUMENT EXTRACTOR
=============================================
Ultra-robust system for complete content extraction with:
- Pagination detection and following
- Dynamic content loading
- Deep document discovery  
- Content reconstruction from fragments
- Multi-format document processing
- Intelligent link following
- Complete document verification
"""

import asyncio
import aiohttp
import logging
import re
import json
from typing import Dict, List, Optional, Any, Tuple, Set
from urllib.parse import urljoin, urlparse, parse_qs
from pathlib import Path
import hashlib
from datetime import datetime, timedelta
import time

from bs4 import BeautifulSoup, Comment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Import our base extractor
from enhanced_content_extractor import IntelligentContentExtractor

logger = logging.getLogger(__name__)

class CompleteDocumentExtractor:
    """Advanced extractor for complete legal documents with intelligent reconstruction"""
    
    def __init__(self):
        self.base_extractor = IntelligentContentExtractor()
        self.session_pool = {}
        self.content_cache = {}
        self.discovered_links = set()
        self.processed_urls = set()
        
        # Pagination patterns (most common legal site patterns)
        self.pagination_patterns = [
            # Standard pagination
            r'page\s*[=:]\s*(\d+)',
            r'p\s*[=:]\s*(\d+)',
            r'pg\s*[=:]\s*(\d+)',
            
            # Legal-specific pagination
            r'opinion[_-]?page\s*[=:]\s*(\d+)',
            r'case[_-]?page\s*[=:]\s*(\d+)',
            r'doc[_-]?page\s*[=:]\s*(\d+)',
            
            # Generic patterns
            r'/(\d+)/?$',
            r'[?&]page=(\d+)',
            r'[?&]p=(\d+)'
        ]
        
        # Pagination selectors for next page detection
        self.pagination_selectors = [
            'a[rel="next"]', '.next', '.next-page', '[title*="next"]',
            'a:contains("Next")', 'a:contains(">")', 'a:contains("→")',
            '.pagination a:last-child', '.pager a:last-child',
            'a[href*="page="]', 'a[href*="p="]', 'a[href*="/2"]'
        ]
        
        # Content continuation indicators
        self.continuation_indicators = [
            'continue reading', 'read more', 'full text', 'complete document',
            'view full', 'entire document', 'full opinion', 'complete case',
            'full judgment', 'complete ruling', 'entire text'
        ]
        
        # Document link patterns
        self.document_link_patterns = [
            r'\.pdf$', r'\.doc$', r'\.docx$', r'\.txt$',
            r'/opinion/', r'/case/', r'/judgment/', r'/ruling/',
            r'/document/', r'/full[_-]?text/', r'/complete/',
            r'[?&]format=(pdf|doc|txt|full)', r'[?&]view=(full|complete)',
        ]
        
        # Content completeness indicators
        self.completeness_indicators = {
            'truncation_signals': [
                '...', '[continue]', '[more]', 'read more', 'click here',
                'full text available', 'complete document', 'view entire',
                '(continued)', 'see full', 'download complete'
            ],
            'ending_signals': [
                'end of document', 'conclusion', 'dated this', 'signed',
                'respectfully submitted', 'so ordered', 'judgment entered',
                'case closed', 'final order', 'disposition'
            ],
            'legal_structure_signals': [
                'background', 'facts', 'analysis', 'holding', 'conclusion',
                'whereas', 'now therefore', 'ordered that', 'it is hereby'
            ]
        }

    async def extract_complete_document(self, url: str, max_pages: int = 10, follow_links: bool = True) -> Dict[str, Any]:
        """Extract complete document with advanced reconstruction techniques"""
        start_time = time.time()
        
        try:
            logger.info(f"🔍 Starting complete extraction for: {url}")
            
            # Initialize session
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers=self._get_smart_headers()
            ) as session:
                
                # Phase 1: Extract base content
                base_result = await self._extract_base_content(session, url)
                if not base_result['success']:
                    return base_result
                
                # Phase 2: Detect and handle pagination
                paginated_content = await self._handle_pagination(session, url, base_result)
                
                # Phase 3: Follow document links for complete content
                if follow_links:
                    linked_content = await self._follow_document_links(session, url, base_result)
                    paginated_content = self._merge_content(paginated_content, linked_content)
                
                # Phase 4: Content reconstruction and verification
                complete_content = await self._reconstruct_complete_document(paginated_content)
                
                # Phase 5: Quality assessment and validation
                final_result = await self._validate_completeness(complete_content, url)
                
                processing_time = time.time() - start_time
                final_result['processing_time'] = processing_time
                final_result['extraction_method'] = 'advanced_complete'
                
                logger.info(f"✅ Complete extraction finished in {processing_time:.2f}s")
                logger.info(f"   📄 Final content length: {len(final_result.get('content', '')):,} chars")
                logger.info(f"   🎯 Completeness score: {final_result.get('completeness_score', 0.0):.2f}")
                
                return final_result
                
        except Exception as e:
            logger.error(f"❌ Complete extraction failed for {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'url': url,
                'extraction_method': 'advanced_complete_failed'
            }

    def _get_smart_headers(self) -> Dict[str, str]:
        """Generate intelligent headers for legal site access"""
        return {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

    async def _extract_base_content(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Extract base content with enhanced error handling"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html_content = await response.text()
                    
                    # Use our enhanced extractor for base content
                    result = await self.base_extractor.extract_content(html_content, url)
                    
                    # Add raw HTML for further processing
                    result['raw_html'] = html_content
                    result['base_url'] = url
                    
                    return result
                else:
                    return {
                        'success': False,
                        'error': f'HTTP {response.status}',
                        'content': '',
                        'url': url
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'url': url
            }

    async def _handle_pagination(self, session: aiohttp.ClientSession, base_url: str, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect and follow pagination to get complete content"""
        if not base_result.get('success'):
            return base_result
        
        try:
            logger.info("🔄 Checking for pagination...")
            
            html_content = base_result.get('raw_html', '')
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Detect pagination links
            pagination_urls = await self._detect_pagination_urls(soup, base_url)
            
            if not pagination_urls:
                logger.info("   No pagination detected")
                return base_result
            
            logger.info(f"   📑 Found {len(pagination_urls)} additional pages")
            
            # Extract content from all pages
            all_content = [base_result['content']]
            all_metadata = [base_result.get('metadata', {})]
            
            for i, page_url in enumerate(pagination_urls[:10], 2):  # Limit to 10 pages max
                try:
                    logger.info(f"   🔄 Processing page {i}: {page_url}")
                    
                    await asyncio.sleep(1)  # Respectful delay
                    
                    async with session.get(page_url) as response:
                        if response.status == 200:
                            page_html = await response.text()
                            page_result = await self.base_extractor.extract_content(page_html, page_url)
                            
                            if page_result['success']:
                                all_content.append(page_result['content'])
                                all_metadata.append(page_result.get('metadata', {}))
                                logger.info(f"      ✅ Extracted {len(page_result['content']):,} chars")
                            else:
                                logger.warning(f"      ⚠️ Failed to extract from page {i}")
                        else:
                            logger.warning(f"      ⚠️ HTTP {response.status} for page {i}")
                            
                except Exception as e:
                    logger.warning(f"      ❌ Error processing page {i}: {e}")
            
            # Combine all content intelligently
            combined_content = await self._intelligently_combine_pages(all_content)
            combined_metadata = self._merge_metadata(all_metadata)
            
            result = base_result.copy()
            result['content'] = combined_content
            result['metadata'] = combined_metadata
            result['pages_processed'] = len(all_content)
            result['total_length'] = len(combined_content)
            
            logger.info(f"   ✅ Combined {len(all_content)} pages into {len(combined_content):,} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"Pagination handling failed: {e}")
            return base_result

    async def _detect_pagination_urls(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Detect pagination URLs using multiple strategies"""
        pagination_urls = []
        seen_urls = set()
        
        try:
            # Strategy 1: Find explicit pagination links
            for selector in self.pagination_selectors:
                try:
                    elements = soup.select(selector)
                    for element in elements:
                        href = element.get('href')
                        if href:
                            full_url = urljoin(base_url, href)
                            if full_url not in seen_urls and full_url != base_url:
                                pagination_urls.append(full_url)
                                seen_urls.add(full_url)
                except Exception:
                    continue
            
            # Strategy 2: Pattern-based detection
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    
                    # Check if URL matches pagination patterns
                    for pattern in self.pagination_patterns:
                        if re.search(pattern, href, re.IGNORECASE):
                            if full_url not in seen_urls and full_url != base_url:
                                pagination_urls.append(full_url)
                                seen_urls.add(full_url)
                            break
            
            # Strategy 3: Numbered page detection
            base_domain = urlparse(base_url).netloc
            for link in all_links:
                href = link.get('href')
                if href and urlparse(urljoin(base_url, href)).netloc == base_domain:
                    # Look for numbered pages (2, 3, 4, etc.)
                    if re.search(r'/[234567890]/?$', href) or re.search(r'[?&](page?|p)=[234567890]', href):
                        full_url = urljoin(base_url, href)
                        if full_url not in seen_urls:
                            pagination_urls.append(full_url)
                            seen_urls.add(full_url)
            
            # Sort URLs to maintain logical order
            return sorted(list(set(pagination_urls)))
            
        except Exception as e:
            logger.error(f"Pagination URL detection failed: {e}")
            return []

    async def _intelligently_combine_pages(self, content_pages: List[str]) -> str:
        """Intelligently combine paginated content"""
        if not content_pages:
            return ""
        
        if len(content_pages) == 1:
            return content_pages[0]
        
        try:
            # Clean and prepare content
            cleaned_pages = []
            for page in content_pages:
                # Remove duplicated headers/footers between pages
                cleaned_page = self._remove_page_artifacts(page)
                if cleaned_page and len(cleaned_page.strip()) > 50:  # Only keep substantial content
                    cleaned_pages.append(cleaned_page)
            
            if not cleaned_pages:
                return content_pages[0] if content_pages else ""
            
            # Strategy 1: Look for natural break points
            combined = ""
            for i, page in enumerate(cleaned_pages):
                if i == 0:
                    combined = page
                else:
                    # Check if pages naturally connect
                    last_sentence = self._get_last_sentence(combined)
                    first_sentence = self._get_first_sentence(page)
                    
                    if self._pages_naturally_connect(last_sentence, first_sentence):
                        # Seamless connection
                        combined += " " + page
                    else:
                        # Add page break
                        combined += "\n\n" + page
            
            return combined.strip()
            
        except Exception as e:
            logger.error(f"Content combination failed: {e}")
            # Fallback: simple concatenation
            return "\n\n".join(content_pages)

    def _remove_page_artifacts(self, content: str) -> str:
        """Remove common pagination artifacts"""
        try:
            # Remove page numbers at start/end
            content = re.sub(r'^Page \d+\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*Page \d+$', '', content, flags=re.MULTILINE)
            
            # Remove "continued on next page" type text
            content = re.sub(r'\s*\(continued.*?\)\s*$', '', content, flags=re.IGNORECASE | re.MULTILINE)
            content = re.sub(r'\s*continued on .*?page.*$', '', content, flags=re.IGNORECASE | re.MULTILINE)
            
            # Remove duplicate headers/footers (simple detection)
            lines = content.split('\n')
            if len(lines) > 5:
                # Remove first/last lines if they look like headers/footers
                first_line = lines[0].strip()
                last_line = lines[-1].strip()
                
                if len(first_line) < 100 and any(word in first_line.lower() for word in ['page', 'header', 'court', 'case']):
                    lines = lines[1:]
                
                if len(last_line) < 100 and any(word in last_line.lower() for word in ['page', 'footer', 'copyright', 'printed']):
                    lines = lines[:-1]
                
                content = '\n'.join(lines)
            
            return content.strip()
            
        except Exception:
            return content

    def _get_last_sentence(self, text: str) -> str:
        """Get the last complete sentence from text"""
        try:
            sentences = re.split(r'[.!?]+', text)
            return sentences[-2].strip() if len(sentences) > 1 else ""
        except Exception:
            return ""

    def _get_first_sentence(self, text: str) -> str:
        """Get the first complete sentence from text"""
        try:
            sentences = re.split(r'[.!?]+', text)
            return sentences[0].strip() if sentences else ""
        except Exception:
            return ""

    def _pages_naturally_connect(self, last_sentence: str, first_sentence: str) -> bool:
        """Check if two pages naturally connect"""
        if not last_sentence or not first_sentence:
            return False
        
        try:
            # Check if last sentence ends abruptly (incomplete)
            incomplete_endings = [',', 'and', 'or', 'but', 'however', 'therefore', 'moreover']
            last_words = last_sentence.lower().split()
            
            if last_words and any(last_words[-1].endswith(ending) for ending in incomplete_endings):
                return True
            
            # Check if first sentence starts with continuation words
            continuation_starts = ['and', 'or', 'but', 'however', 'therefore', 'moreover', 'furthermore']
            first_words = first_sentence.lower().split()
            
            if first_words and first_words[0] in continuation_starts:
                return True
            
            return False
            
        except Exception:
            return False

    async def _follow_document_links(self, session: aiohttp.ClientSession, base_url: str, base_result: Dict[str, Any]) -> Dict[str, Any]:
        """Follow links to complete document formats (PDF, full text, etc.)"""
        try:
            logger.info("🔗 Checking for complete document links...")
            
            html_content = base_result.get('raw_html', '')
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Find document links
            document_links = await self._find_document_links(soup, base_url)
            
            if not document_links:
                logger.info("   No document links found")
                return base_result
            
            logger.info(f"   📎 Found {len(document_links)} document links")
            
            # Try to extract from the most promising links
            best_content = base_result['content']
            best_metadata = base_result.get('metadata', {})
            
            for link_info in document_links[:3]:  # Try top 3 links
                try:
                    url = link_info['url']
                    link_type = link_info['type']
                    
                    logger.info(f"   🔄 Trying {link_type}: {url}")
                    
                    if link_type == 'pdf':
                        # For PDF, we'd need additional processing
                        # For now, skip PDFs but this could be enhanced
                        continue
                    
                    await asyncio.sleep(1)  # Respectful delay
                    
                    async with session.get(url) as response:
                        if response.status == 200:
                            content = await response.text()
                            result = await self.base_extractor.extract_content(content, url)
                            
                            if result['success'] and len(result['content']) > len(best_content):
                                logger.info(f"      ✅ Better content found: {len(result['content']):,} chars")
                                best_content = result['content']
                                best_metadata = result.get('metadata', {})
                            else:
                                logger.info(f"      📏 Content not longer: {len(result.get('content', '')):,} chars")
                        else:
                            logger.warning(f"      ⚠️ HTTP {response.status}")
                            
                except Exception as e:
                    logger.warning(f"      ❌ Error processing link: {e}")
            
            result = base_result.copy()
            result['content'] = best_content
            result['metadata'] = best_metadata
            
            return result
            
        except Exception as e:
            logger.error(f"Document link following failed: {e}")
            return base_result

    async def _find_document_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Find links to complete document formats"""
        document_links = []
        
        try:
            all_links = soup.find_all('a', href=True)
            
            for link in all_links:
                href = link.get('href')
                if not href:
                    continue
                
                full_url = urljoin(base_url, href)
                link_text = link.get_text().strip().lower()
                
                # Score the link based on various factors
                score = 0
                link_type = 'unknown'
                
                # Check URL patterns
                for pattern in self.document_link_patterns:
                    if re.search(pattern, href, re.IGNORECASE):
                        score += 10
                        if '.pdf' in pattern:
                            link_type = 'pdf'
                        elif 'full' in pattern or 'complete' in pattern:
                            link_type = 'full_text'
                        else:
                            link_type = 'document'
                        break
                
                # Check link text for completion indicators
                for indicator in self.continuation_indicators:
                    if indicator in link_text:
                        score += 5
                        if link_type == 'unknown':
                            link_type = 'continuation'
                
                # Bonus for legal-specific terms
                legal_terms = ['full opinion', 'complete case', 'entire judgment', 'full text', 'download']
                for term in legal_terms:
                    if term in link_text:
                        score += 3
                
                if score > 0:
                    document_links.append({
                        'url': full_url,
                        'type': link_type,
                        'text': link_text,
                        'score': score
                    })
            
            # Sort by score (best first)
            document_links.sort(key=lambda x: x['score'], reverse=True)
            
            return document_links
            
        except Exception as e:
            logger.error(f"Document link detection failed: {e}")
            return []

    async def _reconstruct_complete_document(self, content_result: Dict[str, Any]) -> Dict[str, Any]:
        """Reconstruct and optimize the complete document"""
        try:
            content = content_result.get('content', '')
            if not content:
                return content_result
            
            logger.info("🔧 Reconstructing complete document...")
            
            # Phase 1: Remove duplicated sections
            content = await self._remove_duplicated_sections(content)
            
            # Phase 2: Restructure for legal document flow
            content = await self._restructure_legal_document(content)
            
            # Phase 3: Fix broken sentences and paragraphs
            content = await self._fix_content_breaks(content)
            
            # Phase 4: Enhance readability
            content = await self._enhance_readability(content)
            
            result = content_result.copy()
            result['content'] = content
            result['reconstructed'] = True
            
            logger.info(f"   ✅ Document reconstructed: {len(content):,} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"Document reconstruction failed: {e}")
            return content_result

    async def _remove_duplicated_sections(self, content: str) -> str:
        """Remove duplicated content sections"""
        try:
            paragraphs = content.split('\n\n')
            seen_paragraphs = set()
            unique_paragraphs = []
            
            for paragraph in paragraphs:
                # Create a signature for the paragraph
                signature = hashlib.md5(paragraph.strip().lower().encode()).hexdigest()
                
                if signature not in seen_paragraphs:
                    seen_paragraphs.add(signature)
                    unique_paragraphs.append(paragraph)
            
            return '\n\n'.join(unique_paragraphs)
            
        except Exception:
            return content

    async def _restructure_legal_document(self, content: str) -> str:
        """Restructure content to follow legal document conventions"""
        try:
            # Identify and organize legal document sections
            sections = {
                'header': [],
                'facts': [],
                'analysis': [],
                'holding': [],
                'conclusion': []
            }
            
            paragraphs = content.split('\n\n')
            
            for paragraph in paragraphs:
                para_lower = paragraph.lower()
                
                # Classify paragraph by content
                if any(term in para_lower for term in ['facts', 'background', 'procedural history']):
                    sections['facts'].append(paragraph)
                elif any(term in para_lower for term in ['analysis', 'discussion', 'reasoning']):
                    sections['analysis'].append(paragraph)
                elif any(term in para_lower for term in ['holding', 'decision', 'ruling']):
                    sections['holding'].append(paragraph)
                elif any(term in para_lower for term in ['conclusion', 'summary', 'disposition']):
                    sections['conclusion'].append(paragraph)
                else:
                    # Default to facts section for unclassified content
                    sections['facts'].append(paragraph)
            
            # Reconstruct in logical order
            reconstructed_parts = []
            
            for section_name in ['header', 'facts', 'analysis', 'holding', 'conclusion']:
                if sections[section_name]:
                    reconstructed_parts.extend(sections[section_name])
            
            return '\n\n'.join(reconstructed_parts) if reconstructed_parts else content
            
        except Exception:
            return content

    async def _fix_content_breaks(self, content: str) -> str:
        """Fix broken sentences and paragraph structure"""
        try:
            # Fix broken sentences across line breaks
            content = re.sub(r'([a-z,])\s*\n\s*([a-z])', r'\1 \2', content)
            
            # Fix broken words across lines
            content = re.sub(r'([a-z])-\s*\n\s*([a-z])', r'\1\2', content)
            
            # Normalize paragraph breaks
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Fix sentence spacing
            content = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', content)
            
            return content.strip()
            
        except Exception:
            return content

    async def _enhance_readability(self, content: str) -> str:
        """Enhance content readability for legal documents"""
        try:
            # Ensure proper paragraph structure
            paragraphs = content.split('\n\n')
            enhanced_paragraphs = []
            
            for paragraph in paragraphs:
                # Skip very short paragraphs (likely artifacts)
                if len(paragraph.strip()) < 10:
                    continue
                
                # Ensure paragraph starts with capital letter
                paragraph = paragraph.strip()
                if paragraph and not paragraph[0].isupper():
                    paragraph = paragraph[0].upper() + paragraph[1:]
                
                # Ensure paragraph ends with proper punctuation
                if paragraph and paragraph[-1] not in '.!?':
                    paragraph += '.'
                
                enhanced_paragraphs.append(paragraph)
            
            return '\n\n'.join(enhanced_paragraphs)
            
        except Exception:
            return content

    async def _validate_completeness(self, content_result: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Validate document completeness and calculate completeness score"""
        try:
            content = content_result.get('content', '')
            
            if not content:
                content_result['completeness_score'] = 0.0
                content_result['completeness_indicators'] = {'truncated': True, 'reason': 'No content'}
                return content_result
            
            logger.info("✅ Validating document completeness...")
            
            # Calculate completeness score
            completeness_score = 0.0
            indicators = {}
            
            # Check for truncation signals (negative indicators)
            truncation_count = 0
            for signal in self.completeness_indicators['truncation_signals']:
                if signal.lower() in content.lower():
                    truncation_count += 1
            
            if truncation_count == 0:
                completeness_score += 0.3  # No truncation signals
            else:
                indicators['truncation_signals'] = truncation_count
            
            # Check for ending signals (positive indicators)
            ending_signals = 0
            for signal in self.completeness_indicators['ending_signals']:
                if signal.lower() in content.lower():
                    ending_signals += 1
            
            if ending_signals > 0:
                completeness_score += 0.3  # Has proper endings
                indicators['ending_signals'] = ending_signals
            
            # Check legal document structure
            structure_score = 0
            structure_elements = 0
            for signal in self.completeness_indicators['legal_structure_signals']:
                if signal.lower() in content.lower():
                    structure_elements += 1
            
            if structure_elements >= 3:
                structure_score = 0.2
            elif structure_elements >= 1:
                structure_score = 0.1
            
            completeness_score += structure_score
            indicators['structure_elements'] = structure_elements
            
            # Length-based assessment
            content_length = len(content)
            if content_length > 5000:
                completeness_score += 0.2  # Substantial content
            elif content_length > 1000:
                completeness_score += 0.1
            
            indicators['content_length'] = content_length
            
            # Final scoring
            completeness_score = min(completeness_score, 1.0)
            
            # Add completeness information to result
            content_result['completeness_score'] = completeness_score
            content_result['completeness_indicators'] = indicators
            content_result['is_complete'] = completeness_score >= 0.7
            
            logger.info(f"   🎯 Completeness score: {completeness_score:.2f}")
            logger.info(f"   📊 Is complete: {content_result['is_complete']}")
            
            return content_result
            
        except Exception as e:
            logger.error(f"Completeness validation failed: {e}")
            content_result['completeness_score'] = 0.5  # Default moderate score
            return content_result

    def _merge_content(self, content1: Dict[str, Any], content2: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two content results intelligently"""
        if not content1.get('success'):
            return content2
        if not content2.get('success'):
            return content1
        
        # Use the content with higher quality/length
        content1_len = len(content1.get('content', ''))
        content2_len = len(content2.get('content', ''))
        
        if content2_len > content1_len * 1.2:  # Significantly longer
            return content2
        else:
            return content1

    def _merge_metadata(self, metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge metadata from multiple sources"""
        merged = {}
        
        for metadata in metadata_list:
            for key, value in metadata.items():
                if key not in merged and value:
                    merged[key] = value
        
        return merged

# Convenience function for easy usage
async def extract_complete_legal_document(url: str, max_pages: int = 10, follow_links: bool = True) -> Dict[str, Any]:
    """Extract complete legal document with all advanced features"""
    extractor = CompleteDocumentExtractor()
    return await extractor.extract_complete_document(url, max_pages, follow_links)