#!/usr/bin/env python3
"""
🚀 ULTRA-COMPREHENSIVE LEGAL DOCUMENT EXTRACTION LAUNCHER
========================================================
Initiates the massive extraction process for 148M+ legal documents
from 87 ultra-comprehensive global sources across 7 tiers.
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
import signal
import os
from typing import Dict, Any, List
import json

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import ultra-scale components
from ultra_comprehensive_global_sources import (
    ULTRA_COMPREHENSIVE_GLOBAL_SOURCES,
    ULTRA_COMPREHENSIVE_CONFIG, 
    get_comprehensive_statistics,
    get_sources_by_tier,
    get_sources_by_priority
)

from ultra_scale_scraping_engine import (
    UltraScaleScrapingEngine,
    ProcessingMode
)

from ultra_scale_database_service import UltraScaleDatabaseService

# Configure logging for extraction process
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/backend/extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ExtractionController:
    """Controls the massive legal document extraction process"""
    
    def __init__(self):
        self.engine = None
        self.database_service = None
        self.extraction_stats = {
            "start_time": None,
            "documents_processed": 0,
            "documents_saved": 0,
            "sources_completed": 0,
            "current_tier": 1,
            "errors": [],
            "performance_metrics": {}
        }
        self.is_running = False
        
    async def initialize_system(self):
        """Initialize all ultra-scale components"""
        try:
            logger.info("🔧 INITIALIZING ULTRA-SCALE EXTRACTION SYSTEM...")
            
            # Initialize database service
            self.database_service = UltraScaleDatabaseService()
            await self.database_service.initialize_ultra_scale_architecture()
            logger.info("✅ Database service initialized")
            
            # Initialize scraping engine with ultra-comprehensive sources
            self.engine = UltraScaleScrapingEngine()
            await self.engine.initialize_ultra_comprehensive_sources(
                ULTRA_COMPREHENSIVE_GLOBAL_SOURCES
            )
            logger.info("✅ Scraping engine initialized with 87 sources")
            
            # Set up signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            return False
    
    async def start_extraction_process(self):
        """Start the massive legal document extraction process"""
        try:
            logger.info("🚀 STARTING ULTRA-COMPREHENSIVE LEGAL DOCUMENT EXTRACTION")
            logger.info("=" * 70)
            
            # Print extraction overview
            stats = get_comprehensive_statistics()
            logger.info(f"📊 EXTRACTION TARGET: {stats['total_sources']} sources")
            logger.info(f"📄 ESTIMATED DOCUMENTS: {stats['total_estimated_documents']:,}")
            logger.info(f"🎯 PRIORITY SOURCES: {stats['high_priority_sources']}")
            logger.info("")
            
            self.extraction_stats["start_time"] = datetime.utcnow()
            self.is_running = True
            
            # Phase 1: Extract from Tier 1 (US Government) - Highest Priority
            await self._extract_tier(1, "US Government Sources")
            
            # Phase 2: Extract from Tier 2 (Global Legal Systems)  
            await self._extract_tier(2, "Global Legal Systems")
            
            # Phase 3: Extract from Tier 3 (Academic & Research)
            await self._extract_tier(3, "Academic & Research")
            
            # Phase 4: Extract from remaining tiers (4-7)
            for tier in range(4, 8):
                if self.is_running:
                    tier_names = {
                        4: "Legal Journalism",
                        5: "Professional Organizations", 
                        6: "Legal Aid & Public Interest",
                        7: "Specialized & Emerging"
                    }
                    await self._extract_tier(tier, tier_names[tier])
            
            # Final statistics
            await self._generate_final_report()
            
        except Exception as e:
            logger.error(f"❌ Extraction process failed: {e}")
            self.extraction_stats["errors"].append(str(e))
        
        finally:
            self.is_running = False
            logger.info("🏁 EXTRACTION PROCESS COMPLETED")
    
    async def _extract_tier(self, tier_number: int, tier_name: str):
        """Extract documents from a specific tier"""
        if not self.is_running:
            return
            
        logger.info(f"🎯 PHASE {tier_number}: EXTRACTING FROM {tier_name.upper()}")
        logger.info("-" * 50)
        
        self.extraction_stats["current_tier"] = tier_number
        
        # Get sources for this tier
        tier_sources = get_sources_by_tier(tier_number)
        logger.info(f"📊 Tier {tier_number}: {len(tier_sources)} sources")
        
        # Start processing sources in this tier
        processing_mode = ProcessingMode.ULTRA_QUALITY if tier_number <= 2 else ProcessingMode.BALANCED
        
        try:
            # Process tier with intelligent batching
            batch_size = min(10, len(tier_sources))  # Process in batches of 10
            source_ids = list(tier_sources.keys())
            
            for i in range(0, len(source_ids), batch_size):
                if not self.is_running:
                    break
                    
                batch = source_ids[i:i + batch_size]
                logger.info(f"🔄 Processing batch {i//batch_size + 1}: {batch}")
                
                # Process batch of sources concurrently
                results = await self.engine.process_sources_batch(
                    source_ids=batch,
                    processing_mode=processing_mode,
                    max_documents_per_source=10000  # Limit per source for this demo
                )
                
                # Process results and update statistics
                await self._process_batch_results(results, tier_number)
                
                # Brief pause between batches
                await asyncio.sleep(2)
        
        except Exception as e:
            logger.error(f"❌ Error processing tier {tier_number}: {e}")
            self.extraction_stats["errors"].append(f"Tier {tier_number}: {str(e)}")
        
        logger.info(f"✅ TIER {tier_number} COMPLETED: {tier_name}")
        logger.info("")
    
    async def _process_batch_results(self, results: Dict[str, Any], tier: int):
        """Process and save batch results"""
        try:
            documents_in_batch = 0
            
            for source_id, result in results.items():
                if result.get('status') == 'success':
                    documents = result.get('documents', [])
                    
                    # Save documents to database
                    if documents:
                        saved_count = await self.database_service.save_documents_batch(
                            documents, source_id
                        )
                        
                        documents_in_batch += len(documents)
                        self.extraction_stats["documents_processed"] += len(documents)
                        self.extraction_stats["documents_saved"] += saved_count
                        
                        logger.info(f"  ✅ {source_id}: {len(documents)} docs processed, {saved_count} saved")
                    
                    self.extraction_stats["sources_completed"] += 1
                    
                else:
                    error_msg = result.get('error', 'Unknown error')
                    logger.warning(f"  ⚠️ {source_id}: {error_msg}")
            
            # Update performance metrics
            elapsed_time = datetime.utcnow() - self.extraction_stats["start_time"]
            rate = self.extraction_stats["documents_processed"] / max(elapsed_time.total_seconds(), 1)
            
            self.extraction_stats["performance_metrics"] = {
                "documents_per_second": round(rate, 2),
                "elapsed_time_minutes": round(elapsed_time.total_seconds() / 60, 2),
                "estimated_completion_hours": round(
                    (148_375_000 - self.extraction_stats["documents_processed"]) / max(rate * 3600, 1), 2
                )
            }
            
            logger.info(f"📊 BATCH COMPLETE: {documents_in_batch} docs | "
                       f"Rate: {rate:.1f} docs/sec | "
                       f"Total: {self.extraction_stats['documents_processed']:,}")
        
        except Exception as e:
            logger.error(f"❌ Error processing batch results: {e}")
    
    async def _generate_final_report(self):
        """Generate comprehensive final extraction report"""
        logger.info("📊 ULTRA-COMPREHENSIVE EXTRACTION REPORT")
        logger.info("=" * 50)
        
        elapsed = datetime.utcnow() - self.extraction_stats["start_time"]
        
        logger.info(f"⏱️  Total Extraction Time: {elapsed}")
        logger.info(f"📄 Documents Processed: {self.extraction_stats['documents_processed']:,}")
        logger.info(f"💾 Documents Saved: {self.extraction_stats['documents_saved']:,}")
        logger.info(f"📊 Sources Completed: {self.extraction_stats['sources_completed']}/87")
        logger.info(f"📈 Average Rate: {self.extraction_stats['performance_metrics'].get('documents_per_second', 0)} docs/sec")
        
        if self.extraction_stats["errors"]:
            logger.info(f"⚠️  Errors Encountered: {len(self.extraction_stats['errors'])}")
            for error in self.extraction_stats["errors"][:5]:  # Show first 5 errors
                logger.info(f"   - {error}")
        
        # Save report to file
        report_file = f"/app/backend/extraction_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.extraction_stats, f, indent=2, default=str)
        
        logger.info(f"📄 Full report saved: {report_file}")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"🛑 Received signal {signum}, initiating graceful shutdown...")
        self.is_running = False

# Main execution
async def main():
    """Main execution function"""
    controller = ExtractionController()
    
    # Initialize system
    if await controller.initialize_system():
        # Start extraction
        await controller.start_extraction_process()
    else:
        logger.error("❌ System initialization failed, aborting extraction")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("🛑 Extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)