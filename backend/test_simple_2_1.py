#!/usr/bin/env python3
"""
Simplified test for Step 2.1: Basic functionality check
"""

import asyncio
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_basic_functionality():
    """Test basic initialization and configuration"""
    
    print("🚀 BASIC STEP 2.1 FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        # Test 1: Import configuration
        print("\n📊 Testing configuration import...")
        from enhanced_legal_sources_config import (
            get_source_statistics, ULTRA_COMPREHENSIVE_SOURCES, 
            get_sources_by_tier, get_source_config
        )
        
        stats = get_source_statistics()
        print(f"✅ Total Sources: {stats['total_sources']}")
        print(f"✅ Total Documents: {stats['total_estimated_documents']:,}")
        
        # Test 2: Test tier-based source grouping
        print("\n🔍 Testing tier-based source retrieval...")
        for tier in [1, 2, 3, 4]:
            tier_sources = get_sources_by_tier(tier)
            print(f"✅ Tier {tier}: {len(tier_sources)} sources")
        
        # Test 3: Engine initialization
        print("\n🏗️ Testing engine initialization...")
        from ultra_scale_scraping_engine import UltraScaleScrapingEngine
        
        engine = UltraScaleScrapingEngine(max_concurrent_sources=10)
        print(f"✅ Engine initialized with {engine.max_concurrent_sources} max sources")
        
        # Test 4: Component availability
        print("\n🔧 Testing component availability...")
        print(f"✅ Document Processor: {type(engine.document_processor).__name__}")
        print(f"✅ Quality Controller: {type(engine.quality_controller).__name__}")
        print(f"✅ Source Pool Manager: {type(engine.source_pool_manager).__name__}")
        
        print("\n🎉 ALL BASIC TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())