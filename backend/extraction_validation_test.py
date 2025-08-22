#!/usr/bin/env python3
"""
🔍 EXTRACTION VALIDATION TEST
===========================
Deep analysis to determine if we're extracting complete legal documents
or just partial content from legal websites
"""

import asyncio
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from enhanced_content_extractor import IntelligentContentExtractor

class ExtractionValidationTest:
    """Validates the completeness and quality of legal document extraction"""
    
    def __init__(self):
        self.content_extractor = IntelligentContentExtractor()
        self.test_results = {
            'extraction_completeness': {},
            'content_analysis': {},
            'validation_summary': {}
        }
    
    async def run_validation_tests(self):
        """Run comprehensive validation tests"""
        print("🔍 STARTING EXTRACTION VALIDATION TEST")
        print("🎯 Testing extraction completeness and quality")
        print("=" * 60)
        
        # Test 1: SEC RSS Feed (Known working)
        await self._validate_sec_extraction()
        
        # Test 2: Supreme Court Direct Page Test
        await self._validate_supreme_court_extraction()
        
        # Test 3: Test a known legal document URL
        await self._validate_specific_legal_document()
        
        # Test 4: Compare raw vs processed content
        await self._validate_content_processing_quality()
        
        self._generate_validation_report()
    
    async def _validate_sec_extraction(self):
        """Test SEC RSS feed extraction in detail"""
        print("\n🏦 TESTING SEC RSS EXTRACTION COMPLETENESS")
        
        try:
            # Get raw RSS content
            rss_url = "https://www.sec.gov/news/pressreleases.rss"
            response = requests.get(rss_url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; LegalDocumentBot/1.0)'
            })
            
            if response.status_code == 200:
                raw_content = response.text
                raw_length = len(raw_content)
                
                print(f"✅ Raw RSS Content Retrieved: {raw_length:,} characters")
                
                # Process with our enhanced extractor
                extraction_result = await self.content_extractor.extract_content(raw_content, rss_url)
                
                if extraction_result.get('success', False):
                    processed_content = extraction_result.get('content', '')
                    processed_length = len(processed_content)
                    
                    # Calculate content retention
                    retention_ratio = processed_length / max(raw_length, 1)
                    
                    print(f"📊 Processed Content: {processed_length:,} characters")
                    print(f"📈 Content Retention: {retention_ratio:.1%}")
                    print(f"🎯 Quality Score: {extraction_result.get('quality_score', 0):.3f}")
                    
                    # Analyze content structure
                    sentences = processed_content.count('.')
                    legal_terms = sum(1 for term in ['SEC', 'Commission', 'enforcement', 'securities', 'violation'] 
                                    if term.lower() in processed_content.lower())
                    
                    print(f"📝 Sentences Found: {sentences}")
                    print(f"⚖️ Legal Terms: {legal_terms}")
                    
                    # Content completeness analysis
                    has_titles = 'SEC ' in processed_content
                    has_details = len(processed_content.split()) > 50
                    has_structure = sentences > 5
                    
                    completeness_score = sum([has_titles, has_details, has_structure]) / 3
                    
                    self.test_results['extraction_completeness']['sec_rss'] = {
                        'raw_length': raw_length,
                        'processed_length': processed_length,
                        'retention_ratio': retention_ratio,
                        'quality_score': extraction_result.get('quality_score', 0),
                        'completeness_score': completeness_score,
                        'has_structure': has_structure,
                        'legal_content_detected': legal_terms > 0,
                        'content_preview': processed_content[:300]
                    }
                    
                    print(f"📋 Completeness Assessment: {completeness_score:.1%}")
                    
                    if completeness_score > 0.7:
                        print("✅ EXTRACTION QUALITY: EXCELLENT - Complete content extracted")
                    elif completeness_score > 0.4:
                        print("⚠️  EXTRACTION QUALITY: PARTIAL - Some content missing")
                    else:
                        print("❌ EXTRACTION QUALITY: POOR - Minimal content extracted")
                
        except Exception as e:
            print(f"❌ SEC extraction validation failed: {e}")
    
    async def _validate_supreme_court_extraction(self):
        """Test Supreme Court extraction with detailed analysis"""
        print("\n🏛️ TESTING SUPREME COURT EXTRACTION COMPLETENESS")
        
        try:
            # Setup browser
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            service = Service('/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(30)
            
            # Test Supreme Court opinions page
            test_url = "https://www.supremecourt.gov/opinions/boundvolumes/"
            print(f"🌐 Testing URL: {test_url}")
            
            driver.get(test_url)
            time.sleep(3)
            
            # Get raw page source
            raw_html = driver.page_source
            raw_length = len(raw_html)
            
            print(f"📥 Raw HTML Retrieved: {raw_length:,} characters")
            
            # Process with enhanced extractor
            extraction_result = await self.content_extractor.extract_content(raw_html, test_url)
            
            if extraction_result.get('success', False):
                processed_content = extraction_result.get('content', '')
                processed_length = len(processed_content)
                
                retention_ratio = processed_length / max(raw_length, 1)
                
                print(f"📊 Processed Content: {processed_length:,} characters")
                print(f"📈 Content Retention: {retention_ratio:.1%}")
                print(f"🎯 Quality Score: {extraction_result.get('quality_score', 0):.3f}")
                
                # Analyze legal document structure
                legal_indicators = [
                    'supreme court' in processed_content.lower(),
                    'opinion' in processed_content.lower(), 
                    'case' in processed_content.lower(),
                    'court' in processed_content.lower(),
                    len(processed_content.split()) > 100  # Substantial content
                ]
                
                structure_score = sum(legal_indicators) / len(legal_indicators)
                
                print(f"⚖️ Legal Structure Score: {structure_score:.1%}")
                
                # Check if we got navigation vs actual content
                navigation_indicators = processed_content.lower().count('menu') + processed_content.lower().count('navigation')
                content_indicators = processed_content.lower().count('opinion') + processed_content.lower().count('case')
                
                content_vs_nav_ratio = content_indicators / max(navigation_indicators + content_indicators, 1)
                
                print(f"📋 Content vs Navigation Ratio: {content_vs_nav_ratio:.2f}")
                
                self.test_results['extraction_completeness']['supreme_court'] = {
                    'raw_length': raw_length,
                    'processed_length': processed_length,
                    'retention_ratio': retention_ratio,
                    'quality_score': extraction_result.get('quality_score', 0),
                    'structure_score': structure_score,
                    'content_vs_nav_ratio': content_vs_nav_ratio,
                    'extraction_success': extraction_result.get('success', False),
                    'content_preview': processed_content[:500]
                }
                
                if structure_score > 0.6 and content_vs_nav_ratio > 0.3:
                    print("✅ EXTRACTION QUALITY: GOOD - Legal content successfully extracted")
                elif structure_score > 0.3:
                    print("⚠️  EXTRACTION QUALITY: MIXED - Some legal content, may include navigation")
                else:
                    print("❌ EXTRACTION QUALITY: POOR - Mostly navigation/boilerplate content")
            
            else:
                print("❌ Enhanced content extraction failed")
                self.test_results['extraction_completeness']['supreme_court'] = {
                    'extraction_success': False,
                    'error': 'Enhanced extractor failed'
                }
            
            driver.quit()
            
        except Exception as e:
            print(f"❌ Supreme Court validation failed: {e}")
    
    async def _validate_specific_legal_document(self):
        """Test extraction of a specific known legal document"""
        print("\n📄 TESTING SPECIFIC LEGAL DOCUMENT EXTRACTION")
        
        # Test a public legal document (Cornell Law School - known to be accessible)
        test_url = "https://www.law.cornell.edu/constitution/first_amendment"
        
        try:
            response = requests.get(test_url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                raw_html = response.text
                raw_length = len(raw_html)
                
                print(f"📥 Retrieved Constitution Document: {raw_length:,} characters")
                
                extraction_result = await self.content_extractor.extract_content(raw_html, test_url)
                
                if extraction_result.get('success', False):
                    processed_content = extraction_result.get('content', '')
                    processed_length = len(processed_content)
                    
                    # Check for constitutional content
                    constitutional_terms = [
                        'amendment', 'constitution', 'congress', 'law', 'freedom',
                        'speech', 'religion', 'press', 'assembly', 'petition'
                    ]
                    
                    terms_found = sum(1 for term in constitutional_terms 
                                    if term.lower() in processed_content.lower())
                    
                    print(f"📊 Processed Content: {processed_length:,} characters")
                    print(f"📈 Constitutional Terms Found: {terms_found}/{len(constitutional_terms)}")
                    print(f"🎯 Quality Score: {extraction_result.get('quality_score', 0):.3f}")
                    
                    # Check if we got the actual amendment text
                    has_amendment_text = 'congress shall make no law' in processed_content.lower()
                    has_full_text = processed_length > 500
                    
                    completeness = (terms_found / len(constitutional_terms)) * 0.7 + \
                                 (1.0 if has_amendment_text else 0.0) * 0.3
                    
                    print(f"🏛️ First Amendment Text Detected: {'✅' if has_amendment_text else '❌'}")
                    print(f"📋 Overall Completeness: {completeness:.1%}")
                    
                    self.test_results['extraction_completeness']['specific_document'] = {
                        'url': test_url,
                        'raw_length': raw_length,
                        'processed_length': processed_length,
                        'constitutional_terms_found': terms_found,
                        'has_amendment_text': has_amendment_text,
                        'completeness_score': completeness,
                        'quality_score': extraction_result.get('quality_score', 0),
                        'content_sample': processed_content[:400]
                    }
                    
                    if completeness > 0.8:
                        print("✅ DOCUMENT EXTRACTION: EXCELLENT - Complete legal document extracted")
                    elif completeness > 0.5:
                        print("⚠️  DOCUMENT EXTRACTION: GOOD - Most content extracted")
                    else:
                        print("❌ DOCUMENT EXTRACTION: POOR - Incomplete content")
                
        except Exception as e:
            print(f"❌ Specific document validation failed: {e}")
    
    async def _validate_content_processing_quality(self):
        """Test the quality of content processing vs raw content"""
        print("\n🔬 TESTING CONTENT PROCESSING QUALITY")
        
        # Test with sample HTML content that includes legal document structure
        sample_legal_html = '''
        <html>
        <head><title>Legal Document Sample</title></head>
        <body>
            <nav>Navigation Menu | Home | About | Contact</nav>
            <div class="sidebar">Advertisement</div>
            <main>
                <h1>Supreme Court Opinion 2024-001</h1>
                <div class="legal-content">
                    <p>The Supreme Court of the United States hereby renders the following opinion in the matter of Petitioner v. Respondent.</p>
                    <h2>Background</h2>
                    <p>The case involves constitutional interpretation of the First Amendment protection of freedom of speech. The lower court held that the regulation was constitutional, but we reverse this decision.</p>
                    <h2>Legal Analysis</h2>
                    <p>Under strict scrutiny analysis, content-based restrictions on speech must be narrowly tailored to serve a compelling government interest. The regulation in question fails this test because it is overly broad and restricts more speech than necessary.</p>
                    <h2>Holding</h2>
                    <p>We hold that the challenged regulation violates the First Amendment and is therefore unconstitutional. The judgment of the lower court is reversed.</p>
                </div>
            </main>
            <footer>Copyright 2024 | Privacy Policy | Terms of Use</footer>
        </body>
        </html>
        '''
        
        try:
            extraction_result = await self.content_extractor.extract_content(sample_legal_html, "test://legal-document")
            
            if extraction_result.get('success', False):
                processed_content = extraction_result.get('content', '')
                
                # Check what was preserved vs removed
                navigation_removed = 'Navigation Menu' not in processed_content
                advertisement_removed = 'Advertisement' not in processed_content
                footer_removed = 'Copyright 2024' not in processed_content
                
                # Check what legal content was preserved
                title_preserved = 'Supreme Court Opinion' in processed_content
                background_preserved = 'constitutional interpretation' in processed_content
                analysis_preserved = 'strict scrutiny' in processed_content
                holding_preserved = 'First Amendment' in processed_content
                
                content_preservation_score = sum([
                    title_preserved, background_preserved, analysis_preserved, holding_preserved
                ]) / 4
                
                noise_removal_score = sum([
                    navigation_removed, advertisement_removed, footer_removed
                ]) / 3
                
                print(f"📊 Content Preservation Score: {content_preservation_score:.1%}")
                print(f"🧹 Noise Removal Score: {noise_removal_score:.1%}")
                print(f"🎯 Quality Score: {extraction_result.get('quality_score', 0):.3f}")
                
                print(f"\n📋 DETAILED ANALYSIS:")
                print(f"  ✅ Title Preserved: {'Yes' if title_preserved else 'No'}")
                print(f"  ✅ Legal Analysis Preserved: {'Yes' if analysis_preserved else 'No'}")
                print(f"  ✅ Constitutional Content: {'Yes' if holding_preserved else 'No'}")
                print(f"  🧹 Navigation Removed: {'Yes' if navigation_removed else 'No'}")
                print(f"  🧹 Ads Removed: {'Yes' if advertisement_removed else 'No'}")
                print(f"  🧹 Footer Removed: {'Yes' if footer_removed else 'No'}")
                
                self.test_results['content_analysis']['processing_quality'] = {
                    'content_preservation_score': content_preservation_score,
                    'noise_removal_score': noise_removal_score,
                    'overall_quality': extraction_result.get('quality_score', 0),
                    'legal_content_preserved': content_preservation_score > 0.8,
                    'boilerplate_removed': noise_removal_score > 0.8,
                    'processed_content': processed_content
                }
                
                overall_effectiveness = (content_preservation_score + noise_removal_score) / 2
                
                if overall_effectiveness > 0.8:
                    print("✅ PROCESSING EFFECTIVENESS: EXCELLENT - Preserves legal content, removes noise")
                elif overall_effectiveness > 0.6:
                    print("⚠️  PROCESSING EFFECTIVENESS: GOOD - Generally effective with some issues")
                else:
                    print("❌ PROCESSING EFFECTIVENESS: POOR - Issues with content processing")
        
        except Exception as e:
            print(f"❌ Content processing validation failed: {e}")
    
    def _generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*80)
        print("🔍 EXTRACTION VALIDATION REPORT")
        print("="*80)
        
        # Overall assessment
        successful_tests = 0
        total_tests = 0
        
        for test_category, results in self.test_results.items():
            for test_name, test_data in results.items():
                total_tests += 1
                if isinstance(test_data, dict):
                    # Check various success indicators
                    if test_data.get('extraction_success', True) and \
                       test_data.get('completeness_score', 0.5) > 0.4:
                        successful_tests += 1
        
        overall_success_rate = successful_tests / max(total_tests, 1) * 100
        
        print(f"📊 OVERALL EXTRACTION EFFECTIVENESS: {overall_success_rate:.1f}%")
        print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
        
        # Detailed findings
        print(f"\n📋 DETAILED FINDINGS:")
        
        # SEC RSS Analysis
        if 'sec_rss' in self.test_results.get('extraction_completeness', {}):
            sec_data = self.test_results['extraction_completeness']['sec_rss']
            print(f"\n🏦 SEC RSS EXTRACTION:")
            print(f"  Retention Rate: {sec_data.get('retention_ratio', 0):.1%}")
            print(f"  Completeness: {sec_data.get('completeness_score', 0):.1%}")
            print(f"  Assessment: {'✅ Complete' if sec_data.get('completeness_score', 0) > 0.7 else '⚠️ Partial'}")
        
        # Supreme Court Analysis
        if 'supreme_court' in self.test_results.get('extraction_completeness', {}):
            sc_data = self.test_results['extraction_completeness']['supreme_court']
            print(f"\n🏛️ SUPREME COURT EXTRACTION:")
            print(f"  Structure Score: {sc_data.get('structure_score', 0):.1%}")
            print(f"  Content vs Nav: {sc_data.get('content_vs_nav_ratio', 0):.2f}")
            print(f"  Assessment: {'✅ Good' if sc_data.get('structure_score', 0) > 0.5 else '⚠️ Limited'}")
        
        # Processing Quality
        if 'processing_quality' in self.test_results.get('content_analysis', {}):
            pq_data = self.test_results['content_analysis']['processing_quality']
            print(f"\n🔬 CONTENT PROCESSING:")
            print(f"  Content Preservation: {pq_data.get('content_preservation_score', 0):.1%}")
            print(f"  Noise Removal: {pq_data.get('noise_removal_score', 0):.1%}")
            print(f"  Assessment: {'✅ Excellent' if pq_data.get('content_preservation_score', 0) > 0.8 else '⚠️ Needs Improvement'}")
        
        print(f"\n🎯 CONCLUSIONS:")
        if overall_success_rate > 75:
            print("✅ EXTRACTION SYSTEM IS HIGHLY EFFECTIVE")
            print("   • Successfully extracts complete legal document content")
            print("   • Effectively removes navigation and boilerplate content") 
            print("   • Ready for large-scale legal document processing")
        elif overall_success_rate > 50:
            print("⚠️ EXTRACTION SYSTEM IS PARTIALLY EFFECTIVE")
            print("   • Extracts substantial content but may miss some elements")
            print("   • Some noise removal needed for optimal results")
            print("   • Suitable for large-scale processing with monitoring")
        else:
            print("❌ EXTRACTION SYSTEM NEEDS IMPROVEMENT")
            print("   • Limited content extraction effectiveness")
            print("   • Significant optimization required before production use")
        
        print("="*80)

async def main():
    """Main validation test execution"""
    validator = ExtractionValidationTest()
    await validator.run_validation_tests()

if __name__ == "__main__":
    asyncio.run(main())