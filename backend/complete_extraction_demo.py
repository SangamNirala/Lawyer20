#!/usr/bin/env python3
"""
🚀 ULTRA-ROBUST COMPLETE EXTRACTION DEMONSTRATION
=================================================
Showcase the power of complete extraction with:
- Multi-page content aggregation
- Document reconstruction
- Completeness validation
- Advanced legal document processing
"""

import asyncio
import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from browser_setup import DocumentExtractor
from ultra_comprehensive_global_sources import get_sources_by_tier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demonstrate_complete_extraction():
    """Demonstrate the ultra-robust complete extraction capabilities"""
    logger.info("🚀 ULTRA-ROBUST COMPLETE EXTRACTION DEMONSTRATION")
    logger.info("=" * 60)
    logger.info("🌟 ADVANCED FEATURES SHOWCASE:")
    logger.info("   ✅ Pagination Detection & Following")
    logger.info("   ✅ Document Link Discovery & Processing")
    logger.info("   ✅ Content Reconstruction & Deduplication")
    logger.info("   ✅ Completeness Validation & Scoring")
    logger.info("   ✅ Multi-page Content Aggregation")
    logger.info("   ✅ Legal Document Structure Recognition")
    logger.info("")
    
    # Get sample sources for testing
    tier_1_sources = get_sources_by_tier(1)
    test_sources = list(tier_1_sources.items())[:2]  # Test 2 government sources
    
    comparison_results = []
    
    # Test both basic and complete extraction
    for source_id, source_config in test_sources:
        logger.info(f"📖 TESTING SOURCE: {source_config.name}")
        logger.info(f"   🔗 URL: {source_config.base_url}")
        logger.info("")
        
        # Test 1: Basic Enhanced Extraction
        logger.info("   🔧 BASIC Enhanced Extraction:")
        try:
            async with DocumentExtractor(use_complete_extraction=False) as basic_extractor:
                basic_result = await basic_extractor.extract_from_web(source_config)
                
                if basic_result['status'] == 'success':
                    basic_doc = basic_result['documents'][0]
                    logger.info(f"      ✅ SUCCESS")
                    logger.info(f"      📄 Content Length: {basic_doc['content_length']:,} chars")
                    logger.info(f"      🎯 Quality Score: {basic_doc.get('quality_score', 0.0):.2f}")
                    logger.info(f"      📊 Completeness: {basic_doc.get('completeness_score', 0.0):.2f}")
                    logger.info(f"      🔧 Method: {basic_doc['extraction_method']}")
                else:
                    basic_doc = None
                    logger.warning(f"      ❌ FAILED: {basic_result.get('error', 'Unknown error')}")
        except Exception as e:
            basic_doc = None
            logger.error(f"      ❌ ERROR: {e}")
        
        logger.info("")
        
        # Test 2: Complete Ultra-Robust Extraction
        logger.info("   🚀 ULTRA-ROBUST Complete Extraction:")
        try:
            async with DocumentExtractor(use_complete_extraction=True) as complete_extractor:
                complete_result = await complete_extractor.extract_from_web(source_config)
                
                if complete_result['status'] == 'success':
                    complete_doc = complete_result['documents'][0]
                    logger.info(f"      ✅ SUCCESS")
                    logger.info(f"      📄 Content Length: {complete_doc['content_length']:,} chars")
                    logger.info(f"      🎯 Quality Score: {complete_doc.get('quality_score', 0.0):.2f}")
                    logger.info(f"      📊 Completeness Score: {complete_doc.get('completeness_score', 0.0):.2f}")
                    logger.info(f"      🏆 Is Complete: {complete_doc.get('is_complete', False)}")
                    logger.info(f"      📑 Pages Processed: {complete_doc.get('pages_processed', 1)}")
                    logger.info(f"      ⏱️ Processing Time: {complete_doc.get('processing_time', 0.0):.2f}s")
                    logger.info(f"      🔧 Method: {complete_doc['extraction_method']}")
                    
                    # Show advanced features used
                    advanced_features = complete_doc.get('advanced_features', {})
                    if advanced_features:
                        logger.info(f"      🌟 Advanced Features Used:")
                        for feature, used in advanced_features.items():
                            status = "✅" if used else "⏸️"
                            logger.info(f"         {status} {feature.replace('_', ' ').title()}")
                    
                    # Show completeness indicators
                    completeness_indicators = complete_doc.get('completeness_indicators', {})
                    if completeness_indicators:
                        logger.info(f"      📊 Completeness Analysis:")
                        for indicator, value in completeness_indicators.items():
                            logger.info(f"         📈 {indicator.replace('_', ' ').title()}: {value}")
                else:
                    complete_doc = None
                    logger.warning(f"      ❌ FAILED: {complete_result.get('error', 'Unknown error')}")
        except Exception as e:
            complete_doc = None
            logger.error(f"      ❌ ERROR: {e}")
        
        logger.info("")
        
        # Compare Results
        if basic_doc and complete_doc:
            logger.info("   📊 COMPARISON ANALYSIS:")
            
            basic_length = basic_doc['content_length']
            complete_length = complete_doc['content_length']
            improvement_ratio = complete_length / basic_length if basic_length > 0 else float('inf')
            
            basic_completeness = basic_doc.get('completeness_score', 0.0)
            complete_completeness = complete_doc.get('completeness_score', 0.0)
            completeness_improvement = complete_completeness - basic_completeness
            
            logger.info(f"      📈 Content Length Improvement: {improvement_ratio:.1f}x")
            logger.info(f"         Basic: {basic_length:,} chars")
            logger.info(f"         Complete: {complete_length:,} chars")
            logger.info(f"         Gain: +{complete_length - basic_length:,} chars")
            
            logger.info(f"      🎯 Completeness Improvement: +{completeness_improvement:.2f}")
            logger.info(f"         Basic: {basic_completeness:.2f}")
            logger.info(f"         Complete: {complete_completeness:.2f}")
            
            # Quality comparison
            basic_quality = basic_doc.get('quality_score', 0.0)
            complete_quality = complete_doc.get('quality_score', 0.0)
            quality_improvement = complete_quality - basic_quality
            
            logger.info(f"      🏆 Quality Improvement: +{quality_improvement:.2f}")
            logger.info(f"         Basic: {basic_quality:.2f}")
            logger.info(f"         Complete: {complete_quality:.2f}")
            
            # Store comparison results
            comparison_results.append({
                'source': source_config.name,
                'url': source_config.base_url,
                'basic': {
                    'content_length': basic_length,
                    'quality_score': basic_quality,
                    'completeness_score': basic_completeness,
                    'method': basic_doc['extraction_method']
                },
                'complete': {
                    'content_length': complete_length,
                    'quality_score': complete_quality,
                    'completeness_score': complete_completeness,
                    'is_complete': complete_doc.get('is_complete', False),
                    'pages_processed': complete_doc.get('pages_processed', 1),
                    'processing_time': complete_doc.get('processing_time', 0.0),
                    'method': complete_doc['extraction_method'],
                    'advanced_features': complete_doc.get('advanced_features', {})
                },
                'improvements': {
                    'content_ratio': improvement_ratio,
                    'content_gain': complete_length - basic_length,
                    'completeness_gain': completeness_improvement,
                    'quality_gain': quality_improvement
                }
            })
            
            # Show content samples
            logger.info(f"\n      📝 CONTENT SAMPLE COMPARISON:")
            logger.info(f"      🔧 Basic Content Sample:")
            basic_sample = basic_doc['content'][:200] + "..." if len(basic_doc['content']) > 200 else basic_doc['content']
            logger.info(f"         {basic_sample}")
            
            logger.info(f"      🚀 Complete Content Sample:")
            complete_sample = complete_doc['content'][:200] + "..." if len(complete_doc['content']) > 200 else complete_doc['content']
            logger.info(f"         {complete_sample}")
        
        logger.info("")
        logger.info("   " + "="*50)
        logger.info("")
    
    # Generate overall summary
    await generate_demonstration_summary(comparison_results)

async def generate_demonstration_summary(comparison_results):
    """Generate comprehensive demonstration summary"""
    logger.info("🏆 ULTRA-ROBUST COMPLETE EXTRACTION SUMMARY")
    logger.info("=" * 70)
    
    if not comparison_results:
        logger.warning("No comparison results available")
        return
    
    # Calculate aggregate improvements
    total_basic_content = sum(r['basic']['content_length'] for r in comparison_results)
    total_complete_content = sum(r['complete']['content_length'] for r in comparison_results)
    avg_improvement_ratio = sum(r['improvements']['content_ratio'] for r in comparison_results) / len(comparison_results)
    avg_completeness_gain = sum(r['improvements']['completeness_gain'] for r in comparison_results) / len(comparison_results)
    avg_quality_gain = sum(r['improvements']['quality_gain'] for r in comparison_results) / len(comparison_results)
    
    successful_extractions = len(comparison_results)
    complete_documents = sum(1 for r in comparison_results if r['complete']['is_complete'])
    avg_pages_processed = sum(r['complete']['pages_processed'] for r in comparison_results) / len(comparison_results)
    avg_processing_time = sum(r['complete']['processing_time'] for r in comparison_results) / len(comparison_results)
    
    logger.info(f"📊 AGGREGATE IMPROVEMENTS:")
    logger.info(f"   📈 Average Content Improvement: {avg_improvement_ratio:.1f}x")
    logger.info(f"   📄 Total Content Extracted:")
    logger.info(f"      Basic: {total_basic_content:,} characters")
    logger.info(f"      Complete: {total_complete_content:,} characters") 
    logger.info(f"      Net Gain: +{total_complete_content - total_basic_content:,} characters")
    
    logger.info(f"\n🎯 QUALITY & COMPLETENESS:")
    logger.info(f"   📊 Average Completeness Gain: +{avg_completeness_gain:.2f}")
    logger.info(f"   🏆 Average Quality Gain: +{avg_quality_gain:.2f}")
    logger.info(f"   ✅ Complete Documents: {complete_documents}/{successful_extractions}")
    logger.info(f"   📑 Average Pages Processed: {avg_pages_processed:.1f}")
    logger.info(f"   ⏱️ Average Processing Time: {avg_processing_time:.2f}s")
    
    logger.info(f"\n🌟 ADVANCED FEATURES UTILIZATION:")
    feature_usage = {}
    for result in comparison_results:
        features = result['complete'].get('advanced_features', {})
        for feature, used in features.items():
            if feature not in feature_usage:
                feature_usage[feature] = 0
            if used:
                feature_usage[feature] += 1
    
    for feature, count in feature_usage.items():
        percentage = (count / len(comparison_results)) * 100
        logger.info(f"   ✅ {feature.replace('_', ' ').title()}: {count}/{len(comparison_results)} ({percentage:.0f}%)")
    
    logger.info(f"\n📋 INDIVIDUAL SOURCE RESULTS:")
    for i, result in enumerate(comparison_results, 1):
        logger.info(f"   {i}. {result['source']}")
        logger.info(f"      📈 Content: {result['improvements']['content_ratio']:.1f}x improvement")
        logger.info(f"      🎯 Completeness: +{result['improvements']['completeness_gain']:.2f}")
        logger.info(f"      🏆 Complete Document: {result['complete']['is_complete']}")
        logger.info(f"      📑 Pages: {result['complete']['pages_processed']}")
    
    # Save demonstration report
    demonstration_report = {
        'demonstration_timestamp': datetime.utcnow().isoformat(),
        'system_version': 'ultra_robust_complete_v1.0',
        'sources_tested': len(comparison_results),
        'aggregate_metrics': {
            'avg_content_improvement_ratio': avg_improvement_ratio,
            'total_basic_content': total_basic_content,
            'total_complete_content': total_complete_content,
            'net_content_gain': total_complete_content - total_basic_content,
            'avg_completeness_gain': avg_completeness_gain,
            'avg_quality_gain': avg_quality_gain,
            'complete_documents_ratio': complete_documents / successful_extractions,
            'avg_pages_processed': avg_pages_processed,
            'avg_processing_time': avg_processing_time
        },
        'feature_utilization': feature_usage,
        'detailed_results': comparison_results
    }
    
    report_file = f"/app/backend/complete_extraction_demo_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(demonstration_report, f, indent=2)
    
    logger.info(f"\n📄 Demonstration report saved: {report_file}")
    
    logger.info(f"\n🎉 TRANSFORMATION COMPLETE!")
    logger.info(f"Your legal document scraper now features:")
    logger.info(f"   🚀 Ultra-robust complete content extraction")
    logger.info(f"   📑 Automatic pagination detection and following")
    logger.info(f"   🔗 Intelligent document link discovery")
    logger.info(f"   🔧 Advanced content reconstruction")
    logger.info(f"   ✅ Comprehensive completeness validation")
    logger.info(f"   📊 Quality assessment and scoring")
    logger.info(f"   🏆 Perfect for legal chatbot knowledge bases")

async def main():
    """Main demonstration execution"""
    await demonstrate_complete_extraction()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Demonstration interrupted by user")
    except Exception as e:
        logger.error(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()