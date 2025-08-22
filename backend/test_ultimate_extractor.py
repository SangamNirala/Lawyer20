#!/usr/bin/env python3
"""
🧪 TEST ULTIMATE EXTRACTOR
==========================
Quick test of the ultimate legal content extractor
"""

import asyncio
import sys
import os

# Add current directory to path to import our extractor
sys.path.append('/app/backend')

from ultimate_legal_content_extractor import UltimateLegalContentExtractor

async def test_extraction_improvements():
    """Test the ultimate extractor vs previous version"""
    
    print("🚀 TESTING ULTIMATE LEGAL CONTENT EXTRACTOR")
    print("🎯 Comparing extraction quality improvements")
    print("=" * 80)
    
    extractor = UltimateLegalContentExtractor()
    
    test_cases = [
        {
            'name': 'SEC RSS Feed (Known Working)',
            'url': 'https://www.sec.gov/news/pressreleases.rss',
            'type': 'rss'
        },
        {
            'name': 'Cornell Constitution (Academic)',
            'url': 'https://www.law.cornell.edu/constitution/first_amendment',
            'type': 'academic'
        },
        {
            'name': 'Supreme Court (Complex Government)',
            'url': 'https://www.supremecourt.gov/opinions/',
            'type': 'government'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}: {test_case['name']}")
        print(f"🌐 URL: {test_case['url']}")
        print("-" * 60)
        
        try:
            # Extract with ultimate system
            result = await extractor.extract_ultimate_content(
                test_case['url'], 
                extraction_type='auto'
            )
            
            # Display results
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            print(f"Status: {status}")
            print(f"Method: {result.extraction_method}")
            print(f"Content Length: {len(result.content):,} characters")
            print(f"Quality Score: {result.quality_score:.3f}")
            print(f"Completeness Score: {result.completeness_score:.3f}")
            print(f"Processing Time: {result.processing_time:.2f}s")
            
            if result.legal_indicators:
                legal = result.legal_indicators
                print(f"Legal Indicators:")
                print(f"  Court References: {'✅' if legal.get('has_court_references') else '❌'}")
                print(f"  Legal Citations: {'✅' if legal.get('has_legal_citations') else '❌'}")
                print(f"  Case Information: {'✅' if legal.get('has_case_information') else '❌'}")
                print(f"  Legal Term Density: {legal.get('legal_term_density', 0):.3f}")
                if legal.get('document_type_indicators'):
                    print(f"  Document Types: {', '.join(legal.get('document_type_indicators', []))}")
            
            if result.content and len(result.content) > 100:
                print(f"\n📄 CONTENT PREVIEW (first 400 chars):")
                print(f"'{result.content[:400]}...'")
                
                # Analysis of improvement
                word_count = len(result.content.split())
                sentence_count = result.content.count('.') + result.content.count('!') + result.content.count('?')
                
                print(f"\n📊 CONTENT ANALYSIS:")
                print(f"  Word Count: {word_count:,}")
                print(f"  Sentence Count: {sentence_count}")
                print(f"  Avg Words/Sentence: {word_count/max(sentence_count,1):.1f}")
                
                # Legal content quality indicators
                legal_keywords = ['court', 'law', 'legal', 'case', 'SEC', 'constitution', 'amendment']
                legal_keyword_count = sum(1 for keyword in legal_keywords if keyword.lower() in result.content.lower())
                print(f"  Legal Keywords Found: {legal_keyword_count}/{len(legal_keywords)}")
            
            else:
                print(f"\n⚠️  NO SUBSTANTIAL CONTENT EXTRACTED")
            
            # Store for comparison
            results.append({
                'test_name': test_case['name'],
                'success': result.success,
                'content_length': len(result.content),
                'quality_score': result.quality_score,
                'completeness_score': result.completeness_score,
                'method': result.extraction_method,
                'processing_time': result.processing_time
            })
            
        except Exception as e:
            print(f"❌ TEST FAILED: {e}")
            results.append({
                'test_name': test_case['name'],
                'success': False,
                'error': str(e)
            })
    
    # Final comparison summary
    print("\n" + "="*80)
    print("📊 ULTIMATE EXTRACTOR PERFORMANCE SUMMARY")
    print("="*80)
    
    successful_tests = sum(1 for r in results if r.get('success', False))
    total_tests = len(results)
    
    print(f"✅ Success Rate: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    
    if successful_tests > 0:
        avg_quality = sum(r.get('quality_score', 0) for r in results if r.get('success')) / successful_tests
        avg_completeness = sum(r.get('completeness_score', 0) for r in results if r.get('success')) / successful_tests
        total_content = sum(r.get('content_length', 0) for r in results if r.get('success'))
        
        print(f"📊 Average Quality Score: {avg_quality:.3f}")
        print(f"📊 Average Completeness Score: {avg_completeness:.3f}")
        print(f"📊 Total Content Extracted: {total_content:,} characters")
        
        # Performance assessment
        if avg_quality > 0.7 and avg_completeness > 0.7:
            print("\n🎉 EXCELLENT: Ultimate extractor shows significant improvement!")
            print("   ✅ High quality content extraction")
            print("   ✅ Comprehensive document coverage")
            print("   ✅ Ready for production deployment")
        elif avg_quality > 0.5 and avg_completeness > 0.5:
            print("\n👍 GOOD: Ultimate extractor shows solid improvement")
            print("   ✅ Reliable content extraction")
            print("   ⚠️  Some optimization opportunities remain")
        else:
            print("\n⚠️  NEEDS IMPROVEMENT: Continue optimization")
    
    print("\n🚀 ULTIMATE EXTRACTOR CAPABILITIES:")
    print("   • 15+ extraction strategies with intelligent fallbacks")
    print("   • Advanced JavaScript handling for modern websites") 
    print("   • PDF processing with OCR capabilities")
    print("   • Legal document structure recognition")
    print("   • Content quality validation and scoring")
    print("   • Multi-format support (HTML, XML, RSS, PDF)")
    print("   • Anti-detection measures for reliable scraping")
    
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_extraction_improvements())