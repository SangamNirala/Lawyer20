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
    
    async def test_step_3_1_ultra_scale_database_architecture(self):
        """Test Step 3.1: Ultra-Scale Database Architecture implementation"""
        print("\n🗄️ TESTING STEP 3.1: ULTRA-SCALE DATABASE ARCHITECTURE")
        print("=" * 60)
        
        try:
            from ultra_scale_database_service import UltraScaleDatabaseService, GeographicShardingStrategy
            from legal_models import LegalDocument, LegalDocumentCreate, DocumentType, JurisdictionLevel
            
            # Test 1: Database service initialization
            try:
                mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
                db_service = UltraScaleDatabaseService(mongo_url)
                
                self.log_test_result(
                    "UltraScaleDatabaseService Initialization",
                    True,
                    "Database service initialized successfully"
                )
                
            except Exception as e:
                self.log_test_result(
                    "UltraScaleDatabaseService Initialization",
                    False,
                    f"Database service initialization failed: {str(e)}",
                    critical=True
                )
                return
            
            # Test 2: Geographic sharding strategy
            sharding_strategy = db_service.sharding_strategy
            expected_shards = [
                'us_federal', 'us_state', 'european_union', 'commonwealth',
                'asia_pacific', 'academic', 'professional', 'specialized'
            ]
            
            actual_shards = list(sharding_strategy.shard_configurations.keys())
            missing_shards = [shard for shard in expected_shards if shard not in actual_shards]
            
            self.log_test_result(
                "Geographic Sharding Strategy",
                len(missing_shards) == 0,
                f"Found {len(actual_shards)} shards, Missing: {missing_shards}",
                critical=True
            )
            
            # Test 3: Shard capacity verification
            total_capacity = sum(
                config.estimated_capacity 
                for config in sharding_strategy.shard_configurations.values()
            )
            expected_min_capacity = 300_000_000  # Should handle 300M+ documents
            
            self.log_test_result(
                "Shard Capacity Verification",
                total_capacity >= expected_min_capacity,
                f"Total capacity: {total_capacity:,} documents (expected >= {expected_min_capacity:,})",
                critical=True
            )
            
            # Test 4: Database architecture initialization
            try:
                await db_service.initialize_ultra_scale_architecture()
                
                self.log_test_result(
                    "Ultra-Scale Architecture Initialization",
                    True,
                    "Database architecture initialized with all shards and indexes"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Ultra-Scale Architecture Initialization",
                    False,
                    f"Architecture initialization failed: {str(e)}",
                    critical=True
                )
                return
            
            # Test 5: Document routing logic
            test_documents = [
                LegalDocumentCreate(
                    title="Test US Federal Case",
                    content="Test content for US federal case",
                    document_type=DocumentType.CASE_LAW,
                    jurisdiction="United States Federal",
                    jurisdiction_level=JurisdictionLevel.FEDERAL,
                    source="test_source",
                    source_url="https://example.com/test1"
                ),
                LegalDocumentCreate(
                    title="Test EU Regulation",
                    content="Test content for EU regulation",
                    document_type=DocumentType.REGULATION,
                    jurisdiction="European Union",
                    jurisdiction_level=JurisdictionLevel.INTERNATIONAL,
                    source="test_source",
                    source_url="https://example.com/test2"
                )
            ]
            
            routing_tests = []
            for doc in test_documents:
                target_shard = sharding_strategy.determine_shard(doc)
                routing_tests.append(target_shard in expected_shards)
                print(f"    📍 Document '{doc.title}' routed to shard: {target_shard}")
            
            self.log_test_result(
                "Document Routing Logic",
                all(routing_tests),
                f"Successfully routed {len(test_documents)} test documents to appropriate shards"
            )
            
            # Test 6: Index creation verification
            index_count = 0
            for shard_name, collection in db_service.collections.items():
                try:
                    index_info = await collection.index_information()
                    shard_indexes = len([name for name in index_info.keys() if not name.startswith('_')])
                    index_count += shard_indexes
                    print(f"    🔧 Shard '{shard_name}': {shard_indexes} indexes created")
                except Exception as e:
                    print(f"    ❌ Failed to check indexes for shard '{shard_name}': {e}")
            
            expected_min_indexes = len(expected_shards) * 10  # At least 10 indexes per shard
            
            self.log_test_result(
                "Ultra-Scale Index Creation",
                index_count >= expected_min_indexes,
                f"Created {index_count} total indexes across all shards (expected >= {expected_min_indexes})"
            )
            
            # Test 7: Document creation and retrieval
            try:
                # Create a test document
                test_doc = test_documents[0]
                created_doc = await db_service.create_document(test_doc)
                
                self.log_test_result(
                    "Document Creation",
                    created_doc.id is not None,
                    f"Successfully created document with ID: {created_doc.id}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Document Creation",
                    False,
                    f"Document creation failed: {str(e)}",
                    critical=True
                )
            
            # Test 8: Bulk document operations
            try:
                bulk_docs = test_documents * 2  # Create 4 test documents
                document_ids = await db_service.create_documents_bulk(bulk_docs)
                
                self.log_test_result(
                    "Bulk Document Operations",
                    len(document_ids) == len(bulk_docs),
                    f"Successfully created {len(document_ids)} documents in bulk"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Bulk Document Operations",
                    False,
                    f"Bulk document creation failed: {str(e)}",
                    critical=True
                )
            
            # Test 9: Performance monitoring
            performance_metrics = db_service.performance_metrics
            
            self.log_test_result(
                "Performance Monitoring",
                isinstance(performance_metrics, list),
                f"Performance metrics tracking active with {len(performance_metrics)} recorded metrics"
            )
            
            # Test 10: Connection cleanup
            try:
                await db_service.close_connections()
                
                self.log_test_result(
                    "Connection Cleanup",
                    True,
                    "Database connections closed successfully"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Connection Cleanup",
                    False,
                    f"Connection cleanup failed: {str(e)}"
                )
            
        except ImportError as e:
            self.log_test_result(
                "Step 3.1 Database Service Import",
                False,
                f"Failed to import Step 3.1 components: {str(e)}",
                critical=True
            )
        except Exception as e:
            self.log_test_result(
                "Step 3.1 Ultra-Scale Database Architecture Test",
                False,
                f"Step 3.1 test failed: {str(e)}",
                critical=True
            )
    
    async def test_backend_api_integration(self):
        """Test backend API integration with ultra-scale components"""
        print("\n🌐 TESTING BACKEND API INTEGRATION")
        print("=" * 60)
        
        try:
            import requests
            import json
            
            # Get backend URL from environment
            backend_url = os.environ.get('REACT_APP_BACKEND_URL', 'https://megaindex-legal.preview.emergentagent.com')
            api_base = f"{backend_url}/api"
            
            # Test 1: API health check
            try:
                response = requests.get(f"{api_base}/", timeout=10)
                
                self.log_test_result(
                    "Backend API Health Check",
                    response.status_code == 200,
                    f"API responded with status {response.status_code}"
                )
                
                if response.status_code == 200:
                    api_info = response.json()
                    print(f"    📡 API Version: {api_info.get('version', 'Unknown')}")
                    print(f"    📡 API Status: {api_info.get('status', 'Unknown')}")
                
            except Exception as e:
                self.log_test_result(
                    "Backend API Health Check",
                    False,
                    f"API health check failed: {str(e)}",
                    critical=True
                )
                return
            
            # Test 2: Dashboard stats endpoint
            try:
                response = requests.get(f"{api_base}/dashboard/stats", timeout=10)
                
                self.log_test_result(
                    "Dashboard Stats Endpoint",
                    response.status_code == 200,
                    f"Dashboard stats endpoint responded with status {response.status_code}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Dashboard Stats Endpoint",
                    False,
                    f"Dashboard stats request failed: {str(e)}"
                )
            
            # Test 3: System health endpoint
            try:
                response = requests.get(f"{api_base}/dashboard/health", timeout=10)
                
                self.log_test_result(
                    "System Health Endpoint",
                    response.status_code == 200,
                    f"System health endpoint responded with status {response.status_code}"
                )
                
                if response.status_code == 200:
                    health_data = response.json()
                    print(f"    🏥 Database Status: {health_data.get('database_status', 'Unknown')}")
                    print(f"    🏥 Scraping Service: {health_data.get('scraping_service_status', 'Unknown')}")
                
            except Exception as e:
                self.log_test_result(
                    "System Health Endpoint",
                    False,
                    f"System health request failed: {str(e)}"
                )
            
            # Test 4: Questions endpoint (basic functionality)
            try:
                response = requests.get(f"{api_base}/questions", timeout=10)
                
                self.log_test_result(
                    "Questions Endpoint",
                    response.status_code == 200,
                    f"Questions endpoint responded with status {response.status_code}"
                )
                
            except Exception as e:
                self.log_test_result(
                    "Questions Endpoint",
                    False,
                    f"Questions endpoint request failed: {str(e)}"
                )
            
        except ImportError as e:
            self.log_test_result(
                "Backend API Integration Test",
                False,
                f"Failed to import required modules for API testing: {str(e)}"
            )
        except Exception as e:
            self.log_test_result(
                "Backend API Integration Test",
                False,
                f"API integration test failed: {str(e)}",
                critical=True
            )
    
    async def run_all_tests(self):
        """Run all Step 2.1 tests"""
        print("🚀 STARTING COMPREHENSIVE BACKEND TESTING")
        print("Testing Step 2.1: Massive Concurrent Processing Architecture")
        print("Testing Step 3.1: Ultra-Scale Database Architecture")
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
            self.test_step_3_1_ultra_scale_database_architecture,
            self.test_backend_api_integration
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
        print("🎯 COMPREHENSIVE BACKEND TESTING RESULTS SUMMARY")
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
            print("🎉 BACKEND IMPLEMENTATION: EXCELLENT - Ready for production!")
            return True
        elif success_rate >= 75 and len(self.test_results['critical_issues']) <= 2:
            print("✅ BACKEND IMPLEMENTATION: GOOD - Minor issues to address")
            return True
        else:
            print("❌ BACKEND IMPLEMENTATION: NEEDS WORK - Critical issues found")
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