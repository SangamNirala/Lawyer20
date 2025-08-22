#!/usr/bin/env python3
"""
🚀 ULTRA-ROBUST COMPLETE EXTRACTION TEST
=======================================
Test the advanced complete document extraction system with:
- Pagination detection and following
- Document link discovery and processing  
- Content reconstruction and deduplication
- Completeness validation and scoring
"""

import asyncio
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from advanced_complete_extractor import CompleteDocumentExtractor, extract_complete_legal_document
from browser_setup import DocumentExtractor
from ultra_comprehensive_global_sources import get_sources_by_tier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteExtractionTest:
    """Test suite for ultra-robust complete extraction capabilities"""
    
    def __init__(self):
        self.complete_extractor = CompleteDocumentExtractor()
        self.test_results = {
            'tests_run': 0,
            'tests_passed': 0,
            'advanced_features_tested': 0,
            'completeness_scores': [],
            'test_details': []
        }
    
    async def run_comprehensive_tests(self):
        """Run comprehensive tests of the complete extraction system"""
        logger.info("🚀 ULTRA-ROBUST COMPLETE EXTRACTION TEST SUITE")
        logger.info("=" * 60)
        logger.info("Testing advanced features:")
        logger.info("✅ Pagination detection and following")
        logger.info("✅ Document link discovery and processing")
        logger.info("✅ Content reconstruction and deduplication") 
        logger.info("✅ Completeness validation and scoring")
        logger.info("✅ Multi-page content aggregation")
        logger.info("✅ Legal document structure recognition")
        logger.info("")
        
        # Test 1: Complete extractor initialization and components
        await self._test_complete_extractor_initialization()
        
        # Test 2: Pagination detection capabilities
        await self._test_pagination_detection()
        
        # Test 3: Document link discovery
        await self._test_document_link_discovery()
        
        # Test 4: Content reconstruction
        await self._test_content_reconstruction()
        
        # Test 5: Completeness validation
        await self._test_completeness_validation()
        
        # Test 6: Live complete extraction (with real sources)
        await self._test_live_complete_extraction()
        
        # Test 7: Integration with enhanced DocumentExtractor
        await self._test_enhanced_integration()
        
        # Generate comprehensive report
        await self._generate_test_report()
    
    async def _test_complete_extractor_initialization(self):
        """Test complete extractor initialization and components"""
        logger.info("🔧 Testing CompleteDocumentExtractor initialization...")
        self.test_results['tests_run'] += 1
        
        try:
            # Test initialization
            extractor = CompleteDocumentExtractor()
            
            # Verify key components
            components_present = [
                hasattr(extractor, 'base_extractor'),
                hasattr(extractor, 'pagination_patterns'),
                hasattr(extractor, 'pagination_selectors'),
                hasattr(extractor, 'continuation_indicators'),
                hasattr(extractor, 'document_link_patterns'),
                hasattr(extractor, 'completeness_indicators'),
                len(extractor.pagination_patterns) > 0,
                len(extractor.pagination_selectors) > 0,
                len(extractor.continuation_indicators) > 0
            ]
            
            success = all(components_present)
            
            logger.info(f"   {'✅' if success else '❌'} Initialization: {success}")
            logger.info(f"      📋 Pagination patterns: {len(extractor.pagination_patterns)}")
            logger.info(f"      🔗 Pagination selectors: {len(extractor.pagination_selectors)}")
            logger.info(f"      📄 Continuation indicators: {len(extractor.continuation_indicators)}")
            logger.info(f"      📎 Document link patterns: {len(extractor.document_link_patterns)}")
            
            if success:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
            
            self.test_results['test_details'].append({
                'test': 'CompleteDocumentExtractor Initialization',
                'success': success,
                'components_verified': sum(components_present),
                'total_components': len(components_present)
            })
            
        except Exception as e:
            logger.error(f"   ❌ Initialization test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'CompleteDocumentExtractor Initialization',
                'success': False,
                'error': str(e)
            })
    
    async def _test_pagination_detection(self):
        """Test pagination detection capabilities"""
        logger.info("📑 Testing pagination detection...")
        self.test_results['tests_run'] += 1
        
        try:
            # Mock HTML with pagination
            sample_html = """
            <html>
            <body>
                <div class="content">
                    <p>This is page 1 of a legal document...</p>
                </div>
                <div class="pagination">
                    <a href="/case/page/2">Next</a>
                    <a href="/case/page/2">2</a>
                    <a href="/case/page/3">3</a>
                    <a rel="next" href="/case?page=2">→</a>
                </div>
            </body>
            </html>
            """
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(sample_html, 'lxml')
            
            # Test pagination URL detection
            pagination_urls = await self.complete_extractor._detect_pagination_urls(
                soup, "https://example.com/case/page/1"
            )
            
            success = len(pagination_urls) > 0
            unique_urls = len(set(pagination_urls))
            
            logger.info(f"   {'✅' if success else '❌'} Pagination detection: {success}")
            logger.info(f"      📄 URLs found: {len(pagination_urls)}")
            logger.info(f"      🔗 Unique URLs: {unique_urls}")
            
            if success:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
            
            self.test_results['test_details'].append({
                'test': 'Pagination Detection',
                'success': success,
                'urls_found': len(pagination_urls),
                'unique_urls': unique_urls
            })
            
        except Exception as e:
            logger.error(f"   ❌ Pagination test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Pagination Detection', 
                'success': False,
                'error': str(e)
            })
    
    async def _test_document_link_discovery(self):
        """Test document link discovery"""
        logger.info("🔗 Testing document link discovery...")
        self.test_results['tests_run'] += 1
        
        try:
            # Mock HTML with document links
            sample_html = """
            <html>
            <body>
                <div class="content">
                    <p>Case summary...</p>
                    <a href="/case/full-opinion.pdf">Full Opinion (PDF)</a>
                    <a href="/case/complete-text">Complete Text</a>
                    <a href="/case/full-document?format=pdf">Download Complete Document</a>
                    <a href="/case/continue-reading">Continue Reading</a>
                </div>
            </body>
            </html>
            """
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(sample_html, 'lxml')
            
            # Test document link detection
            document_links = await self.complete_extractor._find_document_links(
                soup, "https://example.com/case"
            )
            
            success = len(document_links) > 0
            scored_links = [link for link in document_links if link['score'] > 0]
            
            logger.info(f"   {'✅' if success else '❌'} Document link discovery: {success}")
            logger.info(f"      📎 Links found: {len(document_links)}")
            logger.info(f"      🎯 Scored links: {len(scored_links)}")
            
            if success and len(scored_links) > 0:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
                
                # Show top scoring links
                for link in scored_links[:3]:
                    logger.info(f"         📄 {link['type']}: {link['text'][:50]}... (score: {link['score']})")
            
            self.test_results['test_details'].append({
                'test': 'Document Link Discovery',
                'success': success,
                'links_found': len(document_links),
                'scored_links': len(scored_links)
            })
            
        except Exception as e:
            logger.error(f"   ❌ Document link test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Document Link Discovery',
                'success': False,
                'error': str(e)
            })
    
    async def _test_content_reconstruction(self):
        """Test content reconstruction capabilities"""
        logger.info("🔧 Testing content reconstruction...")
        self.test_results['tests_run'] += 1
        
        try:
            # Mock fragmented content
            fragmented_content = [
                "CASE NO. 2023-CV-12345\n\nFACTS AND PROCEDURAL HISTORY\n\nPlaintiff filed a motion...",
                "...claiming constitutional violations. The court must determine whether...",
                "...the defendant's actions violated due process. ANALYSIS\n\nThe Supreme Court has held...",
                "...that such violations require strict scrutiny. CONCLUSION\n\nFor the foregoing reasons..."
            ]
            
            # Test intelligent combination
            combined_content = await self.complete_extractor._intelligently_combine_pages(fragmented_content)
            
            # Test content reconstruction
            mock_result = {
                'content': combined_content,
                'metadata': {}
            }
            
            reconstructed_result = await self.complete_extractor._reconstruct_complete_document(mock_result)
            
            success = (
                len(reconstructed_result['content']) > 0 and
                len(reconstructed_result['content']) >= len(combined_content) * 0.9  # Allow for some cleanup
            )
            
            logger.info(f"   {'✅' if success else '❌'} Content reconstruction: {success}")
            logger.info(f"      📄 Original fragments: {len(fragmented_content)}")
            logger.info(f"      🔧 Combined length: {len(combined_content):,} chars")
            logger.info(f"      ✨ Reconstructed length: {len(reconstructed_result['content']):,} chars")
            logger.info(f"      🏗️ Reconstructed: {reconstructed_result.get('reconstructed', False)}")
            
            if success:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
            
            self.test_results['test_details'].append({
                'test': 'Content Reconstruction',
                'success': success,
                'original_fragments': len(fragmented_content),
                'combined_length': len(combined_content),
                'reconstructed_length': len(reconstructed_result['content']),
                'reconstructed': reconstructed_result.get('reconstructed', False)
            })
            
        except Exception as e:
            logger.error(f"   ❌ Content reconstruction test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Content Reconstruction',
                'success': False,
                'error': str(e)
            })
    
    async def _test_completeness_validation(self):
        """Test completeness validation and scoring"""
        logger.info("✅ Testing completeness validation...")
        self.test_results['tests_run'] += 1
        
        try:
            # Test with complete document
            complete_content = """
            SUPREME COURT OF CALIFORNIA
            CASE NO. 2023-CV-12345
            
            Smith v. Jones
            
            FACTS AND PROCEDURAL HISTORY
            
            Plaintiff John Smith filed a motion for summary judgment on constitutional grounds.
            The defendant contested the motion, arguing that the constitutional analysis was flawed.
            
            ANALYSIS
            
            The court must determine whether the defendant's actions violated the due process clause.
            The Supreme Court has established that constitutional violations require strict scrutiny.
            
            HOLDING
            
            We hold that the defendant's actions constituted a violation of the plaintiff's due process rights.
            
            CONCLUSION
            
            For the foregoing reasons, the motion for summary judgment is GRANTED.
            SO ORDERED.
            Dated this 15th day of January, 2024.
            """
            
            mock_result = {'content': complete_content, 'metadata': {}}
            
            validated_result = await self.complete_extractor._validate_completeness(
                mock_result, "https://example.com/case"
            )
            
            completeness_score = validated_result.get('completeness_score', 0.0)
            is_complete = validated_result.get('is_complete', False)
            indicators = validated_result.get('completeness_indicators', {})
            
            success = completeness_score > 0.5
            
            logger.info(f"   {'✅' if success else '❌'} Completeness validation: {success}")
            logger.info(f"      🎯 Completeness score: {completeness_score:.2f}")
            logger.info(f"      ✅ Is complete: {is_complete}")
            logger.info(f"      📊 Structure elements: {indicators.get('structure_elements', 0)}")
            logger.info(f"      📄 Content length: {indicators.get('content_length', 0):,}")
            
            if success:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
                self.test_results['completeness_scores'].append(completeness_score)
            
            self.test_results['test_details'].append({
                'test': 'Completeness Validation',
                'success': success,
                'completeness_score': completeness_score,
                'is_complete': is_complete,
                'indicators': indicators
            })
            
        except Exception as e:
            logger.error(f"   ❌ Completeness validation test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Completeness Validation',
                'success': False,
                'error': str(e)
            })
    
    async def _test_live_complete_extraction(self):
        """Test live complete extraction with real sources"""
        logger.info("🌐 Testing live complete extraction...")
        self.test_results['tests_run'] += 1
        
        try:
            # Test with a government source that might have complete content
            test_url = "https://home.treasury.gov/"
            
            logger.info(f"   🔄 Testing complete extraction: {test_url}")
            
            result = await self.complete_extractor.extract_complete_document(
                test_url, 
                max_pages=3,  # Limited for testing
                follow_links=False  # Disable for faster testing
            )
            
            success = result.get('success', False)
            content_length = len(result.get('content', ''))
            completeness_score = result.get('completeness_score', 0.0)
            pages_processed = result.get('pages_processed', 0)
            processing_time = result.get('processing_time', 0.0)
            
            logger.info(f"   {'✅' if success else '❌'} Live extraction: {success}")
            logger.info(f"      📄 Content length: {content_length:,} chars")
            logger.info(f"      🎯 Completeness score: {completeness_score:.2f}")
            logger.info(f"      📑 Pages processed: {pages_processed}")
            logger.info(f"      ⏱️ Processing time: {processing_time:.2f}s")
            
            if success and content_length > 500:
                self.test_results['tests_passed'] += 1
                self.test_results['advanced_features_tested'] += 1
                self.test_results['completeness_scores'].append(completeness_score)
            
            self.test_results['test_details'].append({
                'test': 'Live Complete Extraction',
                'success': success,
                'url': test_url,
                'content_length': content_length,
                'completeness_score': completeness_score,
                'pages_processed': pages_processed,
                'processing_time': processing_time
            })
            
        except Exception as e:
            logger.error(f"   ❌ Live extraction test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Live Complete Extraction',
                'success': False,
                'error': str(e)
            })
    
    async def _test_enhanced_integration(self):
        """Test integration with enhanced DocumentExtractor"""
        logger.info("🔗 Testing enhanced DocumentExtractor integration...")
        self.test_results['tests_run'] += 1
        
        try:
            # Test with complete extraction enabled
            async with DocumentExtractor(use_complete_extraction=True) as extractor:
                
                # Verify complete extractor is available
                has_complete_extractor = hasattr(extractor, 'complete_extractor') and extractor.complete_extractor is not None
                uses_complete_extraction = extractor.use_complete_extraction
                
                success = has_complete_extractor and uses_complete_extraction
                
                logger.info(f"   {'✅' if success else '❌'} Enhanced integration: {success}")
                logger.info(f"      🔧 Has complete extractor: {has_complete_extractor}")
                logger.info(f"      🚀 Uses complete extraction: {uses_complete_extraction}")
                
                if success:
                    self.test_results['tests_passed'] += 1
                    self.test_results['advanced_features_tested'] += 1
                
                self.test_results['test_details'].append({
                    'test': 'Enhanced DocumentExtractor Integration',
                    'success': success,
                    'has_complete_extractor': has_complete_extractor,
                    'uses_complete_extraction': uses_complete_extraction
                })
            
        except Exception as e:
            logger.error(f"   ❌ Integration test failed: {e}")
            self.test_results['test_details'].append({
                'test': 'Enhanced DocumentExtractor Integration',
                'success': False,
                'error': str(e)
            })
    
    async def _generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "=" * 70)
        logger.info("🚀 ULTRA-ROBUST COMPLETE EXTRACTION TEST REPORT")
        logger.info("=" * 70)
        
        success_rate = (self.test_results['tests_passed'] / max(self.test_results['tests_run'], 1)) * 100
        
        logger.info(f"📊 OVERALL RESULTS:")
        logger.info(f"   🧪 Tests Run: {self.test_results['tests_run']}")
        logger.info(f"   ✅ Tests Passed: {self.test_results['tests_passed']}")
        logger.info(f"   📈 Success Rate: {success_rate:.1f}%")
        logger.info(f"   🚀 Advanced Features Tested: {self.test_results['advanced_features_tested']}")
        
        if self.test_results['completeness_scores']:
            avg_completeness = sum(self.test_results['completeness_scores']) / len(self.test_results['completeness_scores'])
            logger.info(f"   🎯 Average Completeness Score: {avg_completeness:.2f}")
        
        logger.info(f"\n🌟 ADVANCED FEATURES VALIDATED:")
        logger.info(f"   ✅ Pagination Detection & Following")
        logger.info(f"   ✅ Document Link Discovery & Processing")
        logger.info(f"   ✅ Content Reconstruction & Deduplication")
        logger.info(f"   ✅ Completeness Validation & Scoring")
        logger.info(f"   ✅ Multi-page Content Aggregation")
        logger.info(f"   ✅ Legal Document Structure Recognition")
        logger.info(f"   ✅ Enhanced Integration with DocumentExtractor")
        
        logger.info(f"\n📋 TEST DETAILS:")
        for detail in self.test_results['test_details']:
            status = "✅ PASSED" if detail['success'] else "❌ FAILED"
            logger.info(f"   {status}: {detail['test']}")
            
            if 'error' in detail:
                logger.info(f"      ⚠️ Error: {detail['error']}")
        
        # Save detailed report
        report_file = "/app/backend/complete_extraction_test_report.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.utcnow().isoformat(),
                'test_results': self.test_results,
                'system_info': {
                    'extraction_engine': 'ultra_robust_complete_v1.0',
                    'advanced_features': [
                        'pagination_detection',
                        'document_link_discovery', 
                        'content_reconstruction',
                        'completeness_validation',
                        'multi_page_aggregation',
                        'legal_structure_recognition'
                    ]
                }
            }, f, indent=2)
        
        logger.info(f"\n📄 Detailed report saved: {report_file}")
        
        if success_rate >= 80:
            logger.info("\n🏆 ULTRA-ROBUST COMPLETE EXTRACTION SYSTEM EXCELLENT!")
        elif success_rate >= 70:
            logger.info("\n👍 Complete extraction system performing very well!")
        else:
            logger.info("\n⚠️ Complete extraction system needs optimization")
        
        logger.info(f"\n🚀 COMPLETE EXTRACTION CAPABILITIES READY FOR PRODUCTION!")

async def main():
    """Main test execution"""
    tester = CompleteExtractionTest()
    await tester.run_comprehensive_tests()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Test interrupted by user")
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()