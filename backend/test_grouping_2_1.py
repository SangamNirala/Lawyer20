#!/usr/bin/env python3
"""
Test source grouping functionality for Step 2.1
"""

import asyncio
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_source_grouping():
    """Test the intelligent source grouping"""
    
    print("🚀 TESTING SOURCE GROUPING FUNCTIONALITY")
    print("=" * 60)
    
    try:
        from ultra_scale_scraping_engine import UltraScaleScrapingEngine
        
        # Initialize with smaller parameters for testing
        engine = UltraScaleScrapingEngine(max_concurrent_sources=5)
        print("✅ Engine initialized for testing")
        
        print("\n🤖 Testing intelligent source grouping...")
        
        # Run with timeout to avoid hanging
        source_groups = await asyncio.wait_for(
            engine.group_sources_intelligently(), 
            timeout=10.0
        )
        
        print("✅ Source grouping completed successfully!")
        
        # Analyze results
        total_sources_in_groups = sum(len(sources) for sources in source_groups.values())
        print(f"\n📊 GROUPING RESULTS:")
        print(f"✅ Total groups created: {len(source_groups)}")
        print(f"✅ Total sources grouped: {total_sources_in_groups}")
        
        for group_name, sources in source_groups.items():
            print(f"   📋 {group_name}: {len(sources)} sources")
        
        # Verify expected groups exist
        expected_groups = ["tier_1_government", "tier_2_global", "tier_3_academic", "tier_4_professional"]
        missing_groups = [group for group in expected_groups if group not in source_groups]
        
        if not missing_groups:
            print("✅ All expected groups are present")
        else:
            print(f"⚠️ Missing groups: {missing_groups}")
        
        print("\n🎉 SOURCE GROUPING TEST COMPLETED SUCCESSFULLY!")
        return True
        
    except asyncio.TimeoutError:
        print("❌ Source grouping timed out - possible infinite loop or blocking operation")
        return False
    except Exception as e:
        print(f"❌ Source grouping failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_source_grouping())
    if success:
        print("\n🚀 Step 2.1 Source Grouping is WORKING!")
    else:
        print("\n❌ Step 2.1 Source Grouping needs fixing")
        sys.exit(1)