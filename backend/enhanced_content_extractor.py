#!/usr/bin/env python3
"""
🚀 ENHANCED LEGAL CONTENT EXTRACTOR
==================================
Advanced HTML parsing and content extraction for legal documents
Produces clean, readable text suitable for NLP and chatbot knowledge bases
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple, Set
from urllib.parse import urljoin, urlparse
import asyncio

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from bs4.element import Script, Stylesheet
import lxml.html
from lxml import etree
from lxml.html.clean import Cleaner

logger = logging.getLogger(__name__)

class IntelligentContentExtractor:
    """Advanced content extraction with AI-powered heuristics"""
    
    def __init__(self):
        # Content area selectors (prioritized by specificity)
        self.content_selectors = [
            # Legal document specific
            'article.legal-document', '.legal-content', '.document-content', '.case-content',
            '.opinion-content', '.judgment-content', '.decision-content', '.ruling-content',
            
            # Academic and scholarly
            '.article-content', '.paper-content', '.abstract', '.full-text',
            
            # General content areas (most specific first)
            'main article', 'article', 'main .content', '.main-content', '#main-content',
            '.entry-content', '.post-content', '.page-content', '#content',
            '.content-wrapper', '.content-container', '.document-body',
            
            # Fallback to common containers
            'main', '#main', '.main', '.wrapper', '.container',
            
            # Last resort - body content filtering
            'body'
        ]
        
        # Elements to completely remove
        self.removal_tags = {
            'script', 'style', 'noscript', 'iframe', 'embed', 'object',
            'applet', 'audio', 'video', 'canvas', 'svg', 'math',
            'form', 'input', 'button', 'select', 'textarea'
        }
        
        # Navigation and UI elements to remove
        self.navigation_selectors = [
            'nav', '.nav', '.navigation', '.navbar', '.menu', '.breadcrumb',
            'header', '.header', 'footer', '.footer', '.sidebar', '.aside',
            '.advertisement', '.ads', '.ad', '.banner', '.popup', '.modal',
            '.social-media', '.share-buttons', '.comments', '.comment-section',
            '.related-posts', '.recommended', '.tags', '.categories',
            '.search-box', '.search-form', '.login-form', '.subscription',
            '.cookie-notice', '.privacy-notice', '.alert', '.notification'
        ]
        
        # Legal document structure indicators
        self.legal_indicators = [
            'citation', 'case-number', 'court-name', 'judge', 'plaintiff', 'defendant',
            'petitioner', 'respondent', 'appellant', 'appellee', 'docket',
            'opinion', 'judgment', 'ruling', 'decision', 'order', 'statute',
            'regulation', 'code-section', 'amendment'
        ]
        
        # Initialize HTML cleaner
        self.html_cleaner = Cleaner(
            scripts=True, javascript=True, comments=True, style=True,
            links=False, meta=True, page_structure=False, processing_instructions=True,
            embedded=True, frames=True, forms=False, annoying_tags=True,
            remove_tags=['font', 'center', 'big', 'small'],
            safe_attrs_only=False, safe_attrs=frozenset(['href', 'src', 'alt', 'title'])
        )
    
    async def extract_content(self, html_content: str, url: str) -> Dict[str, Any]:
        """Main content extraction method"""
        try:
            if not html_content or len(html_content.strip()) < 50:
                return {
                    'success': False,
                    'error': 'HTML content too short or empty',
                    'content': '',
                    'title': '',
                    'metadata': {}
                }
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'lxml')
            
            if not soup or not soup.body:
                return {
                    'success': False,
                    'error': 'Invalid HTML structure',
                    'content': '',
                    'title': '',
                    'metadata': {}
                }
            
            # Extract metadata
            metadata = await self._extract_metadata(soup, url)
            
            # Extract title
            title = await self._extract_title(soup)
            
            # Clean and prepare soup
            cleaned_soup = await self._clean_html(soup)
            
            # Extract main content
            content = await self._extract_main_content(cleaned_soup)
            
            # Post-process content
            final_content = await self._post_process_content(content, url)
            
            # Validate content quality
            quality_score = await self._assess_content_quality(final_content, title)
            
            result = {
                'success': len(final_content.strip()) > 100,
                'content': final_content,
                'title': title,
                'metadata': metadata,
                'quality_score': quality_score,
                'content_length': len(final_content),
                'extraction_method': 'enhanced_intelligent'
            }
            
            if not result['success']:
                result['error'] = f'Content too short after processing: {len(final_content)} chars'
            
            return result
            
        except Exception as e:
            logger.error(f"Content extraction failed for {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'content': '',
                'title': '',
                'metadata': {}
            }
    
    async def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract document metadata"""
        metadata = {
            'url': url,
            'domain': urlparse(url).netloc,
            'language': None,
            'description': None,
            'keywords': [],
            'author': None,
            'published_date': None,
            'legal_type': None,
            'court': None,
            'case_number': None
        }
        
        try:
            # Language
            html_tag = soup.find('html')
            if html_tag:
                metadata['language'] = html_tag.get('lang', 'en')
            
            # Meta description
            desc_meta = soup.find('meta', attrs={'name': 'description'}) or \
                       soup.find('meta', attrs={'property': 'og:description'})
            if desc_meta:
                metadata['description'] = desc_meta.get('content', '').strip()
            
            # Keywords
            keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
            if keywords_meta:
                keywords = keywords_meta.get('content', '')
                metadata['keywords'] = [k.strip() for k in keywords.split(',') if k.strip()]
            
            # Author
            author_meta = soup.find('meta', attrs={'name': 'author'}) or \
                         soup.find('meta', attrs={'property': 'article:author'})
            if author_meta:
                metadata['author'] = author_meta.get('content', '').strip()
            
            # Legal-specific metadata
            await self._extract_legal_metadata(soup, metadata)
            
        except Exception as e:
            logger.debug(f"Metadata extraction error: {e}")
        
        return metadata
    
    async def _extract_legal_metadata(self, soup: BeautifulSoup, metadata: Dict[str, Any]):
        """Extract legal document specific metadata"""
        try:
            # Look for court information
            court_indicators = ['court', 'tribunal', 'commission', 'board']
            for indicator in court_indicators:
                court_elem = soup.find(text=re.compile(indicator, re.I))
                if court_elem and hasattr(court_elem, 'parent'):
                    court_text = court_elem.parent.get_text().strip()
                    if len(court_text) < 200:  # Reasonable length for court name
                        metadata['court'] = court_text
                        break
            
            # Case number patterns
            case_patterns = [
                r'Case\s+No\.?\s*[:\-]?\s*([A-Z0-9\-]+)',
                r'Docket\s+No\.?\s*[:\-]?\s*([A-Z0-9\-]+)',
                r'Civil\s+Action\s+No\.?\s*[:\-]?\s*([A-Z0-9\-]+)',
                r'Criminal\s+Case\s+No\.?\s*[:\-]?\s*([A-Z0-9\-]+)'
            ]
            
            text_content = soup.get_text()
            for pattern in case_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    metadata['case_number'] = match.group(1).strip()
                    break
                    
        except Exception as e:
            logger.debug(f"Legal metadata extraction error: {e}")
    
    async def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract document title using multiple strategies"""
        title_candidates = []
        
        try:
            # Strategy 1: Legal document specific titles
            legal_title_selectors = [
                'h1.case-title', 'h1.document-title', '.case-name', '.document-name',
                'h1.opinion-title', 'h1.judgment-title', 'h1.decision-title'
            ]
            
            for selector in legal_title_selectors:
                elem = soup.select_one(selector)
                if elem:
                    title_candidates.append(elem.get_text().strip())
            
            # Strategy 2: Standard HTML title patterns
            title_selectors = ['title', 'h1', 'h2.title', '.title', '.page-title', '.entry-title']
            
            for selector in title_selectors:
                elem = soup.select_one(selector)
                if elem:
                    title_text = elem.get_text().strip()
                    if title_text and len(title_text) < 300:  # Reasonable title length
                        title_candidates.append(title_text)
            
            # Strategy 3: Open Graph title
            og_title = soup.find('meta', attrs={'property': 'og:title'})
            if og_title:
                title_candidates.append(og_title.get('content', '').strip())
            
            # Clean and select best title
            for title in title_candidates:
                if title and len(title) > 5 and len(title) < 300:
                    # Remove common prefixes/suffixes
                    clean_title = re.sub(r'\s*[\|\-\–\—]\s*[^|\-\–\—]*$', '', title)
                    clean_title = re.sub(r'^\s*[^|\-\–\—]*[\|\-\–\—]\s*', '', clean_title)
                    return clean_title.strip() or title
            
            return title_candidates[0] if title_candidates else "Legal Document"
            
        except Exception as e:
            logger.debug(f"Title extraction error: {e}")
            return "Legal Document"
    
    async def _clean_html(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Clean HTML by removing unwanted elements"""
        try:
            # Remove unwanted tags completely
            for tag_name in self.removal_tags:
                for tag in soup.find_all(tag_name):
                    tag.decompose()
            
            # Remove navigation and UI elements
            for selector in self.navigation_selectors:
                for elem in soup.select(selector):
                    elem.decompose()
            
            # Remove comments
            for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
                comment.extract()
            
            # Remove empty elements
            for tag in soup.find_all():
                if not tag.get_text(strip=True) and not tag.find('img'):
                    tag.decompose()
            
            # Remove attributes we don't need (keep structure)
            for tag in soup.find_all(True):
                # Keep only essential attributes for content extraction
                attrs_to_keep = ['class', 'id', 'href', 'src', 'alt', 'title']
                new_attrs = {k: v for k, v in tag.attrs.items() if k in attrs_to_keep}
                tag.attrs = new_attrs
            
            return soup
            
        except Exception as e:
            logger.debug(f"HTML cleaning error: {e}")
            return soup
    
    async def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content using intelligent selectors"""
        content_blocks = []
        
        try:
            # Strategy 1: Try content selectors in order of specificity
            for selector in self.content_selectors:
                try:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text(separator=' ', strip=True)
                        if text and len(text) > 200:  # Substantial content
                            content_blocks.append({
                                'text': text,
                                'length': len(text),
                                'selector': selector,
                                'score': await self._score_content_block(element, text)
                            })
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            # Strategy 2: If no good content found, try paragraph extraction
            if not content_blocks:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    combined_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                    if len(combined_text) > 100:
                        content_blocks.append({
                            'text': combined_text,
                            'length': len(combined_text),
                            'selector': 'paragraphs',
                            'score': 0.6
                        })
            
            # Strategy 3: Last resort - body text with intelligent filtering
            if not content_blocks and soup.body:
                body_text = soup.body.get_text(separator=' ', strip=True)
                if len(body_text) > 100:
                    # Filter out obvious navigation and boilerplate
                    filtered_text = await self._filter_boilerplate_text(body_text)
                    if len(filtered_text) > 100:
                        content_blocks.append({
                            'text': filtered_text,
                            'length': len(filtered_text),
                            'selector': 'body-filtered',
                            'score': 0.3
                        })
            
            # Select best content block
            if content_blocks:
                # Sort by score, then by length
                best_block = max(content_blocks, key=lambda x: (x['score'], x['length']))
                return best_block['text']
            else:
                return ""
                
        except Exception as e:
            logger.error(f"Main content extraction failed: {e}")
            return ""
    
    async def _score_content_block(self, element: Tag, text: str) -> float:
        """Score content block for quality assessment"""
        score = 0.0
        
        try:
            # Base score for having content
            if len(text) > 100:
                score += 0.3
            
            # Bonus for legal indicators
            legal_count = sum(1 for indicator in self.legal_indicators 
                            if indicator in element.get('class', []) or 
                               indicator in text.lower())
            score += min(legal_count * 0.1, 0.3)
            
            # Bonus for structured content (paragraphs, lists)
            paragraphs = len(element.find_all('p'))
            lists = len(element.find_all(['ul', 'ol']))
            score += min((paragraphs + lists) * 0.02, 0.2)
            
            # Penalty for too many links (likely navigation)
            links = len(element.find_all('a'))
            link_ratio = links / max(len(text.split()), 1)
            if link_ratio > 0.1:  # More than 10% links
                score -= 0.2
            
            # Bonus for content length (diminishing returns)
            length_bonus = min(len(text) / 10000, 0.2)  # Max 0.2 bonus
            score += length_bonus
            
        except Exception as e:
            logger.debug(f"Content scoring error: {e}")
        
        return max(0.0, min(score, 1.0))
    
    async def _filter_boilerplate_text(self, text: str) -> str:
        """Filter out common boilerplate text patterns"""
        try:
            lines = text.split('\n')
            filtered_lines = []
            
            # Patterns that indicate boilerplate content
            boilerplate_patterns = [
                r'copyright\s+©', r'all rights reserved', r'privacy policy',
                r'terms of service', r'cookie policy', r'contact us',
                r'follow us', r'social media', r'subscribe', r'newsletter',
                r'advertisement', r'sponsored content', r'related articles',
                r'you may also like', r'recommended for you', r'trending',
                r'menu', r'navigation', r'breadcrumb', r'home.*about.*contact'
            ]
            
            for line in lines:
                line = line.strip()
                if len(line) < 10:  # Skip very short lines
                    continue
                
                # Check if line contains boilerplate patterns
                is_boilerplate = any(re.search(pattern, line, re.IGNORECASE) 
                                   for pattern in boilerplate_patterns)
                
                if not is_boilerplate:
                    filtered_lines.append(line)
            
            return '\n'.join(filtered_lines)
            
        except Exception as e:
            logger.debug(f"Boilerplate filtering error: {e}")
            return text
    
    async def _post_process_content(self, content: str, url: str) -> str:
        """Post-process extracted content"""
        try:
            if not content:
                return ""
            
            # Normalize whitespace
            content = re.sub(r'\s+', ' ', content)
            content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
            
            # Remove excessive repetition
            content = re.sub(r'(.{50,}?)\1{2,}', r'\1', content)
            
            # Clean up common artifacts
            content = re.sub(r'^\s*[\|\-\–\—]+\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*[\|\-\–\—]+\s*$', '', content, flags=re.MULTILINE)
            
            # Remove URLs that might have leaked through
            content = re.sub(r'https?://[^\s]+', '', content)
            
            # Clean up legal citations format
            content = re.sub(r'(\d+)\s+([A-Z][a-z]+\.?\s*\d*d?\s+\d+)', r'\1 \2', content)
            
            # Ensure sentences end properly
            content = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', content)
            
            return content.strip()
            
        except Exception as e:
            logger.debug(f"Content post-processing error: {e}")
            return content
    
    async def _assess_content_quality(self, content: str, title: str) -> float:
        """Assess the quality of extracted content"""
        try:
            if not content:
                return 0.0
            
            score = 0.0
            
            # Length assessment (0-0.3)
            length = len(content)
            if length > 5000:
                score += 0.3
            elif length > 1000:
                score += 0.2
            elif length > 500:
                score += 0.1
            
            # Sentence structure (0-0.2)
            sentences = re.split(r'[.!?]+', content)
            valid_sentences = [s for s in sentences if len(s.strip()) > 20]
            sentence_ratio = len(valid_sentences) / max(len(sentences), 1)
            score += sentence_ratio * 0.2
            
            # Legal content indicators (0-0.3)
            legal_terms = [
                'court', 'judge', 'plaintiff', 'defendant', 'statute', 'regulation',
                'case', 'opinion', 'ruling', 'decision', 'law', 'legal', 'jurisdiction'
            ]
            legal_count = sum(1 for term in legal_terms if term in content.lower())
            score += min(legal_count / len(legal_terms), 1.0) * 0.3
            
            # Coherence check (0-0.2)
            # Check for proper capitalization and punctuation
            caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
            if 0.02 <= caps_ratio <= 0.15:  # Reasonable capitalization
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.debug(f"Quality assessment error: {e}")
            return 0.5

class BatchContentExtractor:
    """Batch processing for multiple documents"""
    
    def __init__(self, max_concurrent: int = 10):
        self.extractor = IntelligentContentExtractor()
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def extract_multiple(self, html_contents: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        """Extract content from multiple HTML documents concurrently"""
        async def extract_single(html_content: str, url: str):
            async with self.semaphore:
                return await self.extractor.extract_content(html_content, url)
        
        tasks = [extract_single(html, url) for html, url in html_contents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch extraction failed for item {i}: {result}")
                processed_results.append({
                    'success': False,
                    'error': str(result),
                    'content': '',
                    'title': '',
                    'metadata': {}
                })
            else:
                processed_results.append(result)
        
        return processed_results

# Convenience functions
async def extract_content_from_html(html_content: str, url: str = "") -> Dict[str, Any]:
    """Simple function to extract content from HTML"""
    extractor = IntelligentContentExtractor()
    return await extractor.extract_content(html_content, url)

async def extract_content_batch(html_documents: List[Tuple[str, str]], max_concurrent: int = 10) -> List[Dict[str, Any]]:
    """Extract content from multiple HTML documents"""
    batch_extractor = BatchContentExtractor(max_concurrent)
    return await batch_extractor.extract_multiple(html_documents)