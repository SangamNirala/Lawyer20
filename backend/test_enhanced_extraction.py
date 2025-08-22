#!/usr/bin/env python3
"""
🧪 TEST ENHANCED CONTENT EXTRACTION
==================================
Test the improved HTML content extraction system
"""

import asyncio
import sys
import json
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from enhanced_content_extractor import IntelligentContentExtractor, extract_content_from_html
from browser_setup import DocumentExtractor
from ultra_comprehensive_global_sources import get_sources_by_tier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedExtractionTest:
    """Test enhanced content extraction capabilities"""
    
    def __init__(self):
        self.content_extractor = IntelligentContentExtractor()
        self.test_results = {
            'tests_run': 0,
            'tests_passed': 0,
            'improvements': [],
            'test_details': []
        }
    
    async def test_sample_documents(self):
        """Test extraction on existing sample documents to show improvement"""
        logger.info("🧪 TESTING ENHANCED CONTENT EXTRACTION")
        logger.info("=" * 50)
        
        # Load existing sample documents for comparison
        demo_dir = Path("/app/backend/demo_extracted_documents")
        
        if not demo_dir.exists():
            logger.warning("Demo documents directory not found. Running live extraction test instead.")
            await self.test_live_extraction()
            return
        
        sample_files = list(demo_dir.glob("*.json"))[:5]  # Test first 5 documents
        
        for sample_file in sample_files:
            try:
                with open(sample_file, 'r') as f:
                    old_doc = json.load(f)
                
                # Extract URL and original content
                url = old_doc.get('url', '')
                old_content = old_doc.get('content', '')
                
                logger.info(f"\n🔍 Testing: {sample_file.name}")
                logger.info(f"   📍 URL: {url}")
                
                # Test enhanced extraction if we have HTML content
                if '<html' in old_content.lower() or '<body' in old_content.lower():
                    result = await self.content_extractor.extract_content(old_content, url)
                    
                    # Compare results
                    await self._compare_extraction_results(
                        sample_file.name, old_doc, result, url
                    )
                else:
                    logger.info(f"   ⚠️ Skipping - no HTML content to process")
                
            except Exception as e:
                logger.error(f"   ❌ Test failed: {e}")
                self.test_results['test_details'].append({
                    'file': sample_file.name,
                    'status': 'error',
                    'error': str(e)
                })
        
        await self._generate_test_report()
    
    async def test_live_extraction(self):
        """Test live extraction from a few sources"""
        logger.info("🌐 TESTING LIVE ENHANCED EXTRACTION")
        logger.info("=" * 40)
        
        # Get a few sources for testing
        tier_1_sources = get_sources_by_tier(1)
        test_sources = list(tier_1_sources.items())[:3]  # Test 3 sources
        
        async with DocumentExtractor() as extractor:
            for source_id, source_config in test_sources:
                try:
                    logger.info(f"\n🔗 Testing live extraction: {source_config.name}")
                    
                    result = await extractor.extract_from_web(source_config)
                    
                    if result['status'] == 'success' and result['documents']:
                        doc = result['documents'][0]
                        
                        test_detail = {
                            'source': source_config.name,
                            'url': doc['url'],
                            'title': doc['title'][:100] + '...' if len(doc['title']) > 100 else doc['title'],
                            'content_length': doc['content_length'],
                            'quality_score': doc.get('quality_score', 0.0),
                            'extraction_method': doc.get('extraction_method', 'unknown'),
                            'status': 'success'
                        }
                        
                        logger.info(f"   ✅ SUCCESS")
                        logger.info(f"      📄 Title: {test_detail['title']}")
                        logger.info(f"      📊 Content: {test_detail['content_length']:,} chars")
                        logger.info(f"      🎯 Quality: {test_detail['quality_score']:.2f}")
                        logger.info(f"      🔧 Method: {test_detail['extraction_method']}")
                        
                        self.test_results['tests_passed'] += 1
                        
                        # Show content sample
                        content_sample = doc['content'][:300] + "..." if len(doc['content']) > 300 else doc['content']
                        logger.info(f"      📝 Sample: {content_sample}")
                        
                    else:
                        test_detail = {
                            'source': source_config.name,
                            'status': 'failed',
                            'error': result.get('error', 'Unknown error')
                        }
                        logger.warning(f"   ❌ FAILED: {test_detail['error']}")
                    
                    self.test_results['test_details'].append(test_detail)
                    self.test_results['tests_run'] += 1
                    
                except Exception as e:
                    logger.error(f"   ❌ Exception: {e}")
                    self.test_results['test_details'].append({
                        'source': source_config.name,
                        'status': 'error',
                        'error': str(e)
                    })
                    self.test_results['tests_run'] += 1
        
        await self._generate_test_report()
    
    async def _compare_extraction_results(self, filename: str, old_doc: dict, new_result: dict, url: str):
        """Compare old vs new extraction results"""
        self.test_results['tests_run'] += 1
        
        old_content = old_doc.get('content', '')
        old_title = old_doc.get('title', '')
        
        if new_result['success']:
            new_content = new_result['content']
            new_title = new_result['title']
            
            # Analyze improvements
            improvements = []
            
            # Content quality check
            if '<html' in old_content or '<script' in old_content:
                if '<html' not in new_content and '<script' not in new_content:
                    improvements.append("✅ Removed HTML tags and scripts")
            
            # Length comparison
            old_len = len(old_content)
            new_len = len(new_content)
            
            if new_len > old_len:
                improvements.append(f"📈 Content length increased: {old_len:,} → {new_len:,} chars")
            
            # Title improvement
            if len(new_title) > len(old_title) and "Main Page" not in new_title:
                improvements.append(f"📋 Better title extracted: '{new_title[:50]}...'")
            
            # Quality assessment
            quality_score = new_result.get('quality_score', 0.0)
            if quality_score > 0.7:
                improvements.append(f"🎯 High quality score: {quality_score:.2f}")
            
            test_detail = {
                'file': filename,
                'url': url,
                'status': 'improved',
                'old_length': old_len,
                'new_length': new_len,
                'quality_score': quality_score,
                'improvements': improvements,
                'content_sample': new_content[:200] + "..." if len(new_content) > 200 else new_content
            }
            
            logger.info(f"   ✅ IMPROVED:")
            for improvement in improvements:
                logger.info(f"      {improvement}")
            
            if improvements:
                self.test_results['tests_passed'] += 1
                self.test_results['improvements'].extend(improvements)
            
        else:
            test_detail = {
                'file': filename,
                'url': url,
                'status': 'failed',
                'error': new_result.get('error', 'Unknown error')
            }
            logger.warning(f"   ❌ EXTRACTION FAILED: {test_detail['error']}")
        
        self.test_results['test_details'].append(test_detail)
    
    async def _generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 ENHANCED EXTRACTION TEST REPORT")
        logger.info("=" * 60)
        
        success_rate = (self.test_results['tests_passed'] / max(self.test_results['tests_run'], 1)) * 100
        
        logger.info(f"📈 Overall Results:")
        logger.info(f"   🧪 Tests Run: {self.test_results['tests_run']}")
        logger.info(f"   ✅ Tests Passed: {self.test_results['tests_passed']}")
        logger.info(f"   📊 Success Rate: {success_rate:.1f}%")
        logger.info(f"   🚀 Total Improvements: {len(self.test_results['improvements'])}")
        
        if self.test_results['improvements']:
            logger.info(f"\n🎯 Key Improvements Detected:")
            unique_improvements = list(set(self.test_results['improvements']))
            for improvement in unique_improvements[:10]:  # Show top 10
                logger.info(f"   {improvement}")
        
        # Save detailed report
        report_file = "/app/backend/enhanced_extraction_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        logger.info(f"\n📄 Detailed report saved: {report_file}")
        
        if success_rate >= 70:
            logger.info("🌟 ENHANCED EXTRACTION SYSTEM WORKING EXCELLENTLY!")
        elif success_rate >= 50:
            logger.info("👍 Enhanced extraction system showing good improvements")
        else:
            logger.info("⚠️ Enhanced extraction needs further optimization")

async def main():
    """Main test execution"""
    tester = EnhancedExtractionTest()
    
    # Test existing documents first, then live extraction
    await tester.test_sample_documents()
    
    # Also run a live test
    logger.info("\n" + "=" * 60)
    await tester.test_live_extraction()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()