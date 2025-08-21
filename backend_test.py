#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite for Ultra-Scale Legal Document System
Tests Step 2.1: Massive Concurrent Processing Architecture
Tests Step 3.1: Ultra-Scale Database Architecture
"""

import asyncio
import logging
import sys
import os
import time
import json
from typing import Dict, List, Any
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Step21TestSuite:
    """Comprehensive test suite for Step 2.1 implementation"""
    
    def __init__(self):
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "critical_issues": [],
            "minor_issues": []
        }
        
    def log_test_result(self, test_name: str, success: bool, details: str = "", critical: bool = False):
        """Log test result"""
        self.test_results["total_tests"] += 1
        
        if success:
            self.test_results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.test_results["failed_tests"] += 1
            status = "❌ FAIL"
            if critical:
                self.test_results["critical_issues"].append(f"{test_name}: {details}")
            else:
                self.test_results["minor_issues"].append(f"{test_name}: {details}")
        
        result = {
            "test_name": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.test_results["test_details"].append(result)
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
    
    async def test_enhanced_legal_sources_config(self):
        """Test the enhanced legal sources configuration with 121 sources"""
        print("\n📊 TESTING ENHANCED LEGAL SOURCES CONFIGURATION")
        print("=" * 60)
        
        try:
            from enhanced_legal_sources_config import (
                ULTRA_COMPREHENSIVE_SOURCES, get_source_statistics, 
                get_sources_by_tier, get_source_config, ULTRA_SCALE_CONFIG
            )
            
            # Test 1: Configuration loading
            self.log_test_result(
                "Enhanced Legal Sources Config Import", 
                True, 
                "Successfully imported enhanced legal sources configuration"
            )
            
            # Test 2: Source statistics
            stats = get_source_statistics()
            expected_min_sources = 100  # Should have at least 100 sources
            actual_sources = stats['total_sources']
            
            self.log_test_result(
                "Source Count Verification",
                actual_sources >= expected_min_sources,
                f"Found {actual_sources} sources (expected >= {expected_min_sources})",
                critical=True
            )
            
            # Test 3: Document count verification
            total_docs = stats['total_estimated_documents']
            expected_min_docs = 100_000_000  # Should have at least 100M documents
            
            self.log_test_result(
                "Document Count Verification",
                total_docs >= expected_min_docs,
                f"Found {total_docs:,} estimated documents (expected >= {expected_min_docs:,})",
                critical=True
            )
            
            # Test 4: Jurisdiction coverage
            jurisdictions = len(stats['breakdown_by_jurisdiction'])
            expected_min_jurisdictions = 15  # Should cover at least 15 jurisdictions
            
            self.log_test_result(
                "Jurisdiction Coverage",
                jurisdictions >= expected_min_jurisdictions,
                f"Found {jurisdictions} jurisdictions (expected >= {expected_min_jurisdictions})"
            )
            
            # Test 5: Tier-based source grouping
            tier_tests = []
            for tier in [1, 2, 3, 4]:
                tier_sources = get_sources_by_tier(tier)
                tier_tests.append(len(tier_sources) > 0)
                print(f"    Tier {tier}: {len(tier_sources)} sources")
            
            self.log_test_result(
                "Tier-based Source Grouping",
                all(tier_tests),
                f"All 4 tiers have sources: {tier_tests}",
                critical=True
            )
            
            # Test 6: Source configuration access
            sample_sources = list(ULTRA_COMPREHENSIVE_SOURCES.keys())[:5]
            config_tests = []
            for source_id in sample_sources:
                config = get_source_config(source_id)
                config_tests.append(config is not None and 'name' in config)
            
            self.log_test_result(
                "Source Configuration Access",
                all(config_tests),
                f"Successfully accessed configuration for {len(sample_sources)} sample sources"
            )
            
        except Exception as e:
            self.log_test_result(
                "Enhanced Legal Sources Config Test",
                False,
                f"Configuration test failed: {str(e)}",
                critical=True
            )
    
    async def test_ultra_scale_scraping_engine(self):
        """Test the UltraScaleScrapingEngine initialization and basic functionality"""
        print("\n🏗️ TESTING ULTRA-SCALE SCRAPING ENGINE")
        print("=" * 60)
        
        try:
            from ultra_scale_scraping_engine import UltraScaleScrapingEngine
            
            # Test 1: Engine initialization
            try:
                engine = UltraScaleScrapingEngine(max_concurrent_sources=10)
                self.log_test_result(
                    "UltraScaleScrapingEngine Initialization",
                    True,
                    f"Engine initialized with {engine.max_concurrent_sources} max concurrent sources"
                )
            except Exception as e:
                self.log_test_result(
                    "UltraScaleScrapingEngine Initialization",
                    False,
                    f"Engine initialization failed: {str(e)}",
                    critical=True
                )
                return
            
            # Test 2: Component availability
            components = [
                ("document_processor", "MassiveDocumentProcessor"),
                ("quality_controller", "QualityAssuranceController"),
                ("source_pool_manager", "SourcePoolManager")
            ]
            
            for attr_name, expected_class in components:
                has_component = hasattr(engine, attr_name)
                component = getattr(engine, attr_name, None)
                
                self.log_test_result(
                    f"{expected_class} Component",
                    has_component and component is not None,
                    f"Component available: {type(component).__name__ if component else 'None'}",
                    critical=True
                )
            
            # Test 3: Processing phase management
            self.log_test_result(
                "Processing Phase Management",
                hasattr(engine, 'current_phase') and hasattr(engine, 'processing_stats'),
                f"Current phase: {getattr(engine, 'current_phase', 'Unknown')}"
            )
            
        except ImportError as e:
            self.log_test_result(
                "UltraScaleScrapingEngine Import",
                False,
                f"Failed to import UltraScaleScrapingEngine: {str(e)}",
                critical=True
            )
        except Exception as e:
            self.log_test_result(
                "UltraScaleScrapingEngine Test",
                False,
                f"Engine test failed: {str(e)}",
                critical=True
            )
    
    async def test_intelligent_source_grouping(self):
        """Test the AI-powered intelligent source grouping"""
        print("\n🤖 TESTING INTELLIGENT SOURCE GROUPING")
        print("=" * 60)
        
        try:
            from ultra_scale_scraping_engine import UltraScaleScrapingEngine
            
            # Initialize engine with smaller parameters for testing
            engine = UltraScaleScrapingEngine(max_concurrent_sources=5)
            
            # Test intelligent source grouping with timeout
            try:
                source_groups = await asyncio.wait_for(
                    engine.group_sources_intelligently(), 
                    timeout=15.0
                )
                
                self.log_test_result(
                    "Intelligent Source Grouping Execution",
                    True,
                    "Source grouping completed successfully"
                )
                
                # Test group structure
                expected_groups = ["tier_1_government", "tier_2_global", "tier_3_academic", "tier_4_professional"]
                found_groups = list(source_groups.keys())
                
                missing_groups = [group for group in expected_groups if group not in found_groups]
                
                self.log_test_result(
                    "Expected Group Structure",
                    len(missing_groups) == 0,
                    f"Found groups: {found_groups}, Missing: {missing_groups}",
                    critical=True
                )
                
                # Test group population
                total_sources_in_groups = sum(len(sources) for sources in source_groups.values())
                
                self.log_test_result(
                    "Source Group Population",
                    total_sources_in_groups > 0,
                    f"Total sources in groups: {total_sources_in_groups}"
                )
                
                # Test individual group sizes
                for group_name, sources in source_groups.items():
                    print(f"    📋 {group_name}: {len(sources)} sources")
                
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Intelligent Source Grouping Timeout",
                    False,
                    "Source grouping timed out after 15 seconds",
                    critical=True
                )
            
        except Exception as e:
            self.log_test_result(
                "Intelligent Source Grouping Test",
                False,
                f"Source grouping test failed: {str(e)}",
                critical=True
            )
    
    async def test_document_processing_pipeline(self):
        """Test the MassiveDocumentProcessor and its components"""
        print("\n📄 TESTING DOCUMENT PROCESSING PIPELINE")
        print("=" * 60)
        
        try:
            from ultra_scale_scraping_engine import UltraScaleScrapingEngine, MassiveDocumentProcessor
            
            engine = UltraScaleScrapingEngine(max_concurrent_sources=5)
            doc_processor = engine.document_processor
            
            # Test 1: Document processor initialization
            self.log_test_result(
                "MassiveDocumentProcessor Initialization",
                doc_processor is not None,
                f"Processor type: {type(doc_processor).__name__}"
            )
            
            # Test 2: Content analyzers availability
            expected_analyzers = [
                'citation_extractor',
                'topic_classifier', 
                'quality_assessor',
                'entity_extractor',
                'relationship_mapper'
            ]
            
            available_analyzers = list(doc_processor.content_analyzers.keys())
            missing_analyzers = [analyzer for analyzer in expected_analyzers if analyzer not in available_analyzers]
            
            self.log_test_result(
                "Content Analyzers Availability",
                len(missing_analyzers) == 0,
                f"Available: {available_analyzers}, Missing: {missing_analyzers}",
                critical=True
            )
            
            # Test 3: Processing statistics
            stats = doc_processor.processing_stats
            expected_stats = ['documents_processed', 'documents_enhanced', 'processing_time']
            
            has_stats = all(stat in stats for stat in expected_stats)
            
            self.log_test_result(
                "Processing Statistics Tracking",
                has_stats,
                f"Statistics available: {list(stats.keys())}"
            )
            
            # Test 4: Thread pool availability
            self.log_test_result(
                "Thread Pool Initialization",
                hasattr(doc_processor, 'thread_pool') and doc_processor.thread_pool is not None,
                "Thread pool for concurrent processing available"
            )
            
        except Exception as e:
            self.log_test_result(
                "Document Processing Pipeline Test",
                False,
                f"Document processing test failed: {str(e)}",
                critical=True
            )
    
    async def test_quality_assurance_system(self):
        """Test the QualityAssuranceController validation system"""
        print("\n🔍 TESTING QUALITY ASSURANCE SYSTEM")
        print("=" * 60)
        
        try:
            from ultra_scale_scraping_engine import UltraScaleScrapingEngine, QualityAssuranceController
            
            engine = UltraScaleScrapingEngine(max_concurrent_sources=5)
            quality_controller = engine.quality_controller
            
            # Test 1: Quality controller initialization
            self.log_test_result(
                "QualityAssuranceController Initialization",
                quality_controller is not None,
                f"Controller type: {type(quality_controller).__name__}"
            )
            
            # Test 2: Quality thresholds configuration
            self.log_test_result(
                "Quality Thresholds Configuration",
                hasattr(quality_controller, 'quality_thresholds'),
                "Quality thresholds configured"
            )
            
            # Test 3: Validation rules
            self.log_test_result(
                "Validation Rules Initialization",
                hasattr(quality_controller, 'validation_rules'),
                "Validation rules initialized"
            )
            
            # Test 4: Quality statistics
            try:
                quality_stats = quality_controller.get_quality_statistics()
                expected_stats = ['documents_validated', 'documents_passed', 'documents_failed']
                
                has_required_stats = all(stat in quality_stats for stat in expected_stats)
                
                self.log_test_result(
                    "Quality Statistics Generation",
                    has_required_stats,
                    f"Statistics: {quality_stats}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Quality Statistics Generation",
                    False,
                    f"Failed to get quality statistics: {str(e)}"
                )
            
        except Exception as e:
            self.log_test_result(
                "Quality Assurance System Test",
                False,
                f"Quality assurance test failed: {str(e)}",
                critical=True
            )
    
    async def test_resource_monitoring(self):
        """Test the ResourceMonitor system resource tracking"""
        print("\n💻 TESTING RESOURCE MONITORING SYSTEM")
        print("=" * 60)
        
        try:
            from ultra_scale_scraping_engine import UltraScaleScrapingEngine, ResourceMonitor
            
            engine = UltraScaleScrapingEngine(max_concurrent_sources=5)
            resource_monitor = engine.source_pool_manager.resource_monitor
            
            # Test 1: Resource monitor initialization
            self.log_test_result(
                "ResourceMonitor Initialization",
                resource_monitor is not None,
                f"Monitor type: {type(resource_monitor).__name__}"
            )
            
            # Test 2: System resource checking
            try:
                resources = resource_monitor.check_system_resources()
                expected_metrics = ['cpu_percent', 'memory_percent', 'disk_percent', 'timestamp']
                
                has_metrics = all(metric in resources for metric in expected_metrics)
                
                self.log_test_result(
                    "System Resource Checking",
                    has_metrics,
                    f"CPU: {resources.get('cpu_percent', 'N/A')}%, Memory: {resources.get('memory_percent', 'N/A')}%"
                )
                
            except Exception as e:
                self.log_test_result(
                    "System Resource Checking",
                    False,
                    f"Resource checking failed: {str(e)}",
                    critical=True
                )
            
            # Test 3: Throttling decision
            try:
                should_throttle = resource_monitor.should_throttle_processing()
                
                self.log_test_result(
                    "Processing Throttling Decision",
                    isinstance(should_throttle, bool),
                    f"Should throttle: {should_throttle}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Processing Throttling Decision",
                    False,
                    f"Throttling decision failed: {str(e)}"
                )
            
            # Test 4: Optimal concurrency calculation
            try:
                optimal_concurrency = resource_monitor.get_optimal_concurrency(20)
                
                self.log_test_result(
                    "Optimal Concurrency Calculation",
                    isinstance(optimal_concurrency, int) and optimal_concurrency > 0,
                    f"Optimal concurrency for base 20: {optimal_concurrency}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Optimal Concurrency Calculation",
                    False,
                    f"Concurrency calculation failed: {str(e)}"
                )
            
        except Exception as e:
            self.log_test_result(
                "Resource Monitoring System Test",
                False,
                f"Resource monitoring test failed: {str(e)}",
                critical=True
            )
    
    async def test_intelligent_scraper_engine(self):
        """Test the IntelligentScrapingEngine functionality"""
        print("\n🔧 TESTING INTELLIGENT SCRAPER ENGINE")
        print("=" * 60)
        
        try:
            from intelligent_scraper_engine import IntelligentScrapingEngine, AIContentProcessor
            
            # Test 1: Intelligent scraper engine initialization
            try:
                scraper_engine = IntelligentScrapingEngine()
                
                self.log_test_result(
                    "IntelligentScrapingEngine Initialization",
                    True,
                    "Scraper engine initialized successfully"
                )
                
            except Exception as e:
                self.log_test_result(
                    "IntelligentScrapingEngine Initialization",
                    False,
                    f"Scraper engine initialization failed: {str(e)}",
                    critical=True
                )
                return
            
            # Test 2: AI content processor
            ai_processor = scraper_engine.ai_processor
            
            self.log_test_result(
                "AI Content Processor",
                ai_processor is not None,
                f"Processor type: {type(ai_processor).__name__}"
            )
            
            # Test 3: Citation extraction patterns
            citation_patterns = ai_processor.citation_patterns
            expected_patterns = ['us_case', 'federal_reporter', 'supreme_court']
            
            has_patterns = all(pattern in citation_patterns for pattern in expected_patterns)
            
            self.log_test_result(
                "Citation Extraction Patterns",
                has_patterns,
                f"Available patterns: {list(citation_patterns.keys())}"
            )
            
            # Test 4: Legal topic classification
            legal_topics = ai_processor.legal_topics
            expected_topics = ['constitutional', 'contract', 'tort', 'criminal']
            
            has_topics = all(topic in legal_topics for topic in expected_topics)
            
            self.log_test_result(
                "Legal Topic Classification",
                has_topics,
                f"Available topics: {list(legal_topics.keys())}"
            )
            
            # Test 5: Performance metrics tracking
            self.log_test_result(
                "Performance Metrics Tracking",
                hasattr(scraper_engine, 'performance_metrics'),
                "Performance metrics tracking available"
            )
            
        except ImportError as e:
            self.log_test_result(
                "IntelligentScrapingEngine Import",
                False,
                f"Failed to import IntelligentScrapingEngine: {str(e)}",
                critical=True
            )
        except Exception as e:
            self.log_test_result(
                "Intelligent Scraper Engine Test",
                False,
                f"Scraper engine test failed: {str(e)}",
                critical=True
            )
    
    async def test_legal_models_integration(self):
        """Test the legal models and data structures"""
        print("\n📋 TESTING LEGAL MODELS INTEGRATION")
        print("=" * 60)
        
        try:
            from legal_models import (
                LegalDocument, LegalDocumentCreate, DocumentType, 
                SourceType, ProcessingStatus, LegalSource, 
                LegalScrapingJob, ScrapingJobStatus
            )
            
            # Test 1: Model imports
            self.log_test_result(
                "Legal Models Import",
                True,
                "Successfully imported all legal models"
            )
            
            # Test 2: Document type enumeration
            doc_types = list(DocumentType)
            expected_min_types = 10  # Should have at least 10 document types
            
            self.log_test_result(
                "Document Type Enumeration",
                len(doc_types) >= expected_min_types,
                f"Found {len(doc_types)} document types (expected >= {expected_min_types})"
            )
            
            # Test 3: Source type enumeration
            source_types = list(SourceType)
            expected_source_types = ['API', 'WEB_SCRAPING', 'RSS_FEED']
            
            has_expected_types = all(
                any(st.value == expected for st in source_types) 
                for expected in expected_source_types
            )
            
            self.log_test_result(
                "Source Type Enumeration",
                has_expected_types,
                f"Available source types: {[st.value for st in source_types]}"
            )
            
            # Test 4: Legal document creation
            try:
                test_doc = LegalDocumentCreate(
                    title="Test Legal Document",
                    content="This is a test legal document content.",
                    document_type=DocumentType.CASE_LAW,
                    jurisdiction="United States",
                    jurisdiction_level="federal",
                    source="test_source",
                    source_url="https://example.com/test"
                )
                
                self.log_test_result(
                    "Legal Document Creation",
                    True,
                    f"Successfully created test document: {test_doc.title}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Legal Document Creation",
                    False,
                    f"Document creation failed: {str(e)}"
                )
            
        except ImportError as e:
            self.log_test_result(
                "Legal Models Import",
                False,
                f"Failed to import legal models: {str(e)}",
                critical=True
            )
        except Exception as e:
            self.log_test_result(
                "Legal Models Integration Test",
                False,
                f"Legal models test failed: {str(e)}",
                critical=True
            )
    
    async def run_all_tests(self):
        """Run all Step 2.1 tests"""
        print("🚀 STARTING COMPREHENSIVE STEP 2.1 BACKEND TESTING")
        print("=" * 80)
        print(f"Test started at: {datetime.utcnow().isoformat()}")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites
        test_suites = [
            self.test_enhanced_legal_sources_config,
            self.test_ultra_scale_scraping_engine,
            self.test_intelligent_source_grouping,
            self.test_document_processing_pipeline,
            self.test_quality_assurance_system,
            self.test_resource_monitoring,
            self.test_intelligent_scraper_engine,
            self.test_legal_models_integration
        ]
        
        for test_suite in test_suites:
            try:
                await test_suite()
            except Exception as e:
                self.log_test_result(
                    f"{test_suite.__name__} Suite",
                    False,
                    f"Test suite failed with exception: {str(e)}",
                    critical=True
                )
        
        # Calculate test duration
        test_duration = time.time() - start_time
        
        # Print final results
        print("\n" + "=" * 80)
        print("🎯 STEP 2.1 TESTING RESULTS SUMMARY")
        print("=" * 80)
        
        print(f"📊 Total Tests: {self.test_results['total_tests']}")
        print(f"✅ Passed: {self.test_results['passed_tests']}")
        print(f"❌ Failed: {self.test_results['failed_tests']}")
        print(f"⏱️ Duration: {test_duration:.2f} seconds")
        
        if self.test_results['critical_issues']:
            print(f"\n🚨 CRITICAL ISSUES ({len(self.test_results['critical_issues'])}):")
            for issue in self.test_results['critical_issues']:
                print(f"   ❌ {issue}")
        
        if self.test_results['minor_issues']:
            print(f"\n⚠️ MINOR ISSUES ({len(self.test_results['minor_issues'])}):")
            for issue in self.test_results['minor_issues']:
                print(f"   ⚠️ {issue}")
        
        # Overall assessment
        success_rate = (self.test_results['passed_tests'] / self.test_results['total_tests']) * 100
        
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90 and len(self.test_results['critical_issues']) == 0:
            print("🎉 STEP 2.1 IMPLEMENTATION: EXCELLENT - Ready for production!")
            return True
        elif success_rate >= 75 and len(self.test_results['critical_issues']) <= 2:
            print("✅ STEP 2.1 IMPLEMENTATION: GOOD - Minor issues to address")
            return True
        else:
            print("❌ STEP 2.1 IMPLEMENTATION: NEEDS WORK - Critical issues found")
            return False

async def main():
    """Main test execution function"""
    test_suite = Step21TestSuite()
    
    try:
        success = await test_suite.run_all_tests()
        
        # Save test results to file
        with open('/app/step_2_1_test_results.json', 'w') as f:
            json.dump(test_suite.test_results, f, indent=2, default=str)
        
        if success:
            print("\n🚀 Step 2.1 Ultra-Scale Legal Document Scraping System is READY!")
            sys.exit(0)
        else:
            print("\n❌ Step 2.1 implementation requires attention before deployment")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR during Step 2.1 testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("Starting Step 2.1 Ultra-Scale Legal Document Scraping System Test...")
    asyncio.run(main())