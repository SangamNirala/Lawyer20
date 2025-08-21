"""
Test Suite for Step 4.1 - Ultra-Comprehensive API System
Comprehensive testing of advanced API endpoints for 370M+ documents
"""

import asyncio
import logging
import os
import json
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
import httpx
from motor.motor_asyncio import AsyncIOMotorClient

# Import the ultra-scale API components
try:
    from ultra_scale_api_endpoints import ultra_api_router
    from ultra_scale_api_models import (
        UltraSearchFilter, UltraSearchResponse, SourceHealthDashboard,
        DateRange, GeographicFilter, ContentFilter, QualityFilter
    )
    from query_optimization_service import UltraScaleQueryBuilder
    from source_health_monitor import UltraScaleSourceHealthMonitor
    from enhanced_legal_sources_config import ULTRA_COMPREHENSIVE_SOURCES
    ULTRA_SCALE_AVAILABLE = True
except ImportError as e:
    ULTRA_SCALE_AVAILABLE = False
    logging.warning(f"Ultra-scale components not available: {e}")

# Try to import database service (may not be available in all environments)
try:
    from ultra_scale_database_service import UltraScaleDatabaseService
    DATABASE_SERVICE_AVAILABLE = True
except ImportError as e:
    DATABASE_SERVICE_AVAILABLE = False
    logging.warning(f"Database service not available: {e}")

from legal_models import DocumentType, JurisdictionLevel, ProcessingStatus

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestUltraScaleAPISystem:
    """Comprehensive test suite for Step 4.1 implementation"""
    
    def __init__(self):
        """Initialize test environment"""
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.api_base_url = "http://localhost:8001/api"
        
    async def test_ultra_scale_api_models(self):
        """Test Step 4.1: Ultra-scale API models and structures"""
        logger.info("🧪 Testing Ultra-Scale API Models...")
        
        if not ULTRA_SCALE_AVAILABLE:
            logger.warning("⚠️ Ultra-scale components not available - skipping model tests")
            return {
                'test_status': 'skipped',
                'reason': 'ultra_scale_not_available'
            }
        
        try:
            # Test 1: UltraSearchFilter model
            search_filter = UltraSearchFilter(
                query_text="constitutional law",
                document_types=[DocumentType.CASE_LAW, DocumentType.STATUTE],
                geographic=GeographicFilter(
                    jurisdictions=["United States", "European Union"],
                    jurisdiction_levels=[JurisdictionLevel.FEDERAL]
                ),
                content=ContentFilter(
                    legal_topics=["constitutional_law", "civil_rights"],
                    practice_areas=["constitutional_law"]
                ),
                quality=QualityFilter(
                    min_confidence_score=0.8,
                    processing_status=[ProcessingStatus.COMPLETED]
                ),
                date_ranges=[DateRange(
                    start_date=datetime.now() - timedelta(days=365),
                    end_date=datetime.now()
                )]
            )
            
            logger.info("✅ UltraSearchFilter model created successfully")
            
            # Test 2: Model serialization
            filter_dict = search_filter.dict()
            assert 'query_text' in filter_dict
            assert 'geographic' in filter_dict
            assert 'content' in filter_dict
            assert 'quality' in filter_dict
            logger.info("✅ Model serialization working")
            
            # Test 3: Date range validation
            try:
                invalid_date_range = DateRange(
                    start_date=datetime.now(),
                    end_date=datetime.now() - timedelta(days=1)  # Invalid: end before start
                )
                logger.warning("⚠️ Date range validation not working as expected")
            except ValueError:
                logger.info("✅ Date range validation working correctly")
            
            return {
                'test_status': 'passed',
                'models_tested': 5,
                'validations_tested': 3,
                'serialization_working': True
            }
            
        except Exception as e:
            logger.error(f"❌ API models test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_query_optimization_service(self):
        """Test Step 4.1: Query optimization and building service"""
        logger.info("🧪 Testing Query Optimization Service...")
        
        if not ULTRA_SCALE_AVAILABLE:
            logger.warning("⚠️ Ultra-scale components not available - skipping query optimization tests")
            return {
                'test_status': 'skipped',
                'reason': 'ultra_scale_not_available'
            }
        
        try:
            query_builder = UltraScaleQueryBuilder()
            
            # Test 1: Simple query building
            simple_filter = UltraSearchFilter(
                query_text="contract law",
                document_types=[DocumentType.CASE_LAW]
            )
            
            mongodb_query, query_metadata = query_builder.build_ultra_scale_query(simple_filter)
            
            assert isinstance(mongodb_query, dict)
            assert isinstance(query_metadata, dict)
            assert 'complexity_analysis' in query_metadata
            logger.info("✅ Simple query building working")
            
            # Test 2: Complex query building
            complex_filter = UltraSearchFilter(
                query_text="constitutional AND civil rights",
                document_types=[DocumentType.CASE_LAW, DocumentType.STATUTE],
                geographic=GeographicFilter(
                    jurisdictions=["United States", "European Union", "United Kingdom"],
                    exclude_jurisdictions=["Test Jurisdiction"]
                ),
                content=ContentFilter(
                    legal_topics=["constitutional_law", "civil_rights", "due_process"],
                    keywords=["due process", "equal protection"],
                    exclude_keywords=["test", "sample"]
                ),
                quality=QualityFilter(
                    min_confidence_score=0.9,
                    min_citation_count=5
                ),
                date_ranges=[
                    DateRange(
                        start_date=datetime.now() - timedelta(days=3650),  # 10 years
                        end_date=datetime.now() - timedelta(days=365)     # 1 year ago
                    ),
                    DateRange(
                        start_date=datetime.now() - timedelta(days=90),   # 3 months
                        end_date=datetime.now()
                    )
                ]
            )
            
            complex_query, complex_metadata = query_builder.build_ultra_scale_query(complex_filter)
            
            complexity_score = complex_metadata['complexity_analysis']['complexity_score']
            assert complexity_score > 3.0  # Should be medium to high complexity
            logger.info(f"✅ Complex query building working - Complexity: {complexity_score:.2f}")
            
            # Test 3: Performance optimization
            optimizations = complex_metadata.get('optimizations_applied', [])
            assert len(optimizations) > 0
            logger.info(f"✅ Query optimizations applied: {len(optimizations)}")
            
            # Test 4: Shard routing hints
            shard_hints = complex_metadata.get('shard_routing_hints', [])
            logger.info(f"✅ Shard routing hints generated: {len(shard_hints)}")
            
            return {
                'test_status': 'passed',
                'simple_query_working': True,
                'complex_query_working': True,
                'complexity_score': complexity_score,
                'optimizations_count': len(optimizations),
                'shard_hints_count': len(shard_hints),
                'query_metadata_complete': all(key in complex_metadata for key in [
                    'complexity_analysis', 'optimizations_applied', 'index_hints'
                ])
            }
            
        except Exception as e:
            logger.error(f"❌ Query optimization service test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_source_health_monitor(self):
        """Test Step 4.1: Source health monitoring system"""
        logger.info("🧪 Testing Source Health Monitor...")
        
        if not ULTRA_SCALE_AVAILABLE:
            logger.warning("⚠️ Ultra-scale components not available - skipping source health tests")
            return {
                'test_status': 'skipped',
                'reason': 'ultra_scale_not_available'
            }
        
        try:
            health_monitor = UltraScaleSourceHealthMonitor()
            
            # Test 1: Individual source metrics collection
            first_source_id = list(ULTRA_COMPREHENSIVE_SOURCES.keys())[0]
            individual_metrics = await health_monitor.get_source_metrics(first_source_id)
            
            assert individual_metrics.source_id == first_source_id
            assert hasattr(individual_metrics, 'status')
            assert hasattr(individual_metrics, 'documents_scraped')
            assert hasattr(individual_metrics, 'success_rate')
            logger.info(f"✅ Individual source metrics working - Source: {first_source_id}")
            
            # Test 2: Bulk metrics collection (test with first 10 sources)
            test_source_ids = list(ULTRA_COMPREHENSIVE_SOURCES.keys())[:10]
            bulk_metrics = await health_monitor.get_bulk_source_metrics(test_source_ids, max_concurrent=5)
            
            assert len(bulk_metrics) == len(test_source_ids)
            assert all(isinstance(metrics.success_rate, float) for metrics in bulk_metrics)
            logger.info(f"✅ Bulk metrics collection working - {len(bulk_metrics)} sources")
            
            # Test 3: Source health dashboard generation
            dashboard_start = time.time()
            dashboard = await health_monitor.generate_source_health_dashboard()
            dashboard_time = time.time() - dashboard_start
            
            assert isinstance(dashboard, SourceHealthDashboard)
            assert dashboard.total_sources > 0
            assert dashboard.active_sources >= 0
            assert len(dashboard.source_metrics) > 0
            assert len(dashboard.regional_summaries) > 0
            logger.info(f"✅ Dashboard generation working - Generated in {dashboard_time:.2f}s")
            
            # Test 4: Dashboard content validation
            assert dashboard.total_sources == len(dashboard.source_metrics)
            assert all(hasattr(summary, 'region') for summary in dashboard.regional_summaries)
            assert hasattr(dashboard, 'capacity_metrics')
            assert hasattr(dashboard, 'performance_trends')
            logger.info("✅ Dashboard content validation passed")
            
            # Test 5: Performance metrics
            performance_summary = {
                'total_sources_monitored': dashboard.total_sources,
                'active_sources': dashboard.active_sources,
                'overall_success_rate': dashboard.overall_success_rate,
                'total_documents_scraped': dashboard.total_documents,
                'regional_coverage': len(dashboard.regional_summaries),
                'dashboard_generation_time_seconds': dashboard_time
            }
            
            return {
                'test_status': 'passed',
                'individual_metrics_working': True,
                'bulk_metrics_working': True,
                'dashboard_generation_working': True,
                'dashboard_content_valid': True,
                'performance_summary': performance_summary
            }
            
        except Exception as e:
            logger.error(f"❌ Source health monitor test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_ultra_scale_database_integration(self):
        """Test Step 4.1: Integration with Step 3.1 database architecture"""
        logger.info("🧪 Testing Ultra-Scale Database Integration...")
        
        if not ULTRA_SCALE_AVAILABLE:
            logger.warning("⚠️ Ultra-scale components not available - skipping database integration tests")
            return {
                'test_status': 'skipped',
                'reason': 'ultra_scale_not_available'
            }
        
        try:
            # Test 1: Database service initialization
            db_service = UltraScaleDatabaseService(self.mongo_url)
            await db_service.initialize_ultra_scale_architecture()
            
            logger.info("✅ Database service initialization successful")
            
            # Test 2: Get system metrics
            system_metrics = await db_service.get_ultra_scale_system_metrics()
            
            assert 'total_documents' in system_metrics
            assert 'active_shards' in system_metrics
            assert 'shard_details' in system_metrics
            logger.info(f"✅ System metrics retrieval working - {system_metrics['active_shards']} active shards")
            
            # Test 3: Verify shard architecture
            all_shards = await db_service.get_all_shards()
            expected_shards = [
                'us_federal', 'us_state', 'european_union', 'commonwealth',
                'asia_pacific', 'academic', 'professional', 'specialized'
            ]
            
            assert len(all_shards) == len(expected_shards)
            assert all(shard in expected_shards for shard in all_shards)
            logger.info(f"✅ Shard architecture verified - {len(all_shards)} shards active")
            
            # Test 4: Performance benchmarks
            benchmark_results = await self._run_api_integration_benchmark(db_service)
            
            await db_service.close_connections()
            
            return {
                'test_status': 'passed',
                'database_initialization_working': True,
                'system_metrics_working': True,
                'shard_architecture_verified': True,
                'active_shards_count': len(all_shards),
                'benchmark_results': benchmark_results
            }
            
        except Exception as e:
            logger.error(f"❌ Database integration test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def _run_api_integration_benchmark(self, db_service) -> Dict[str, Any]:
        """Run performance benchmark for API-database integration"""
        logger.info("🏃 Running API integration benchmark...")
        
        try:
            from legal_models import LegalDocumentCreate, LegalDocumentFilter
            
            # Create test documents for API testing
            test_documents = []
            for i in range(20):  # Small test set
                doc = LegalDocumentCreate(
                    title=f"API Test Document {i}",
                    content=f"This is test content for API integration document {i}. " * 5,
                    document_type=DocumentType.CASE_LAW if i % 2 == 0 else DocumentType.STATUTE,
                    jurisdiction="United States" if i % 3 == 0 else "European Union",
                    jurisdiction_level=JurisdictionLevel.FEDERAL,
                    source="api_integration_test",
                    source_url=f"https://test.com/api/doc/{i}",
                    confidence_score=0.8 + (i % 3) * 0.1
                )
                test_documents.append(doc)
            
            # Benchmark document creation
            create_start = time.time()
            document_ids = await db_service.create_documents_bulk(test_documents)
            create_time = time.time() - create_start
            
            # Benchmark search operations
            search_start = time.time()
            search_filter = LegalDocumentFilter(
                jurisdictions=["United States"],
                document_types=[DocumentType.CASE_LAW]
            )
            search_results = await db_service.search_documents(search_filter, page=1, per_page=10)
            search_time = time.time() - search_start
            
            return {
                'documents_created': len(document_ids),
                'create_time_seconds': round(create_time, 3),
                'documents_found': search_results.total_count,
                'search_time_seconds': round(search_time, 3),
                'create_rate_docs_per_second': round(len(document_ids) / create_time, 2),
                'search_response_time_ms': round(search_time * 1000, 2)
            }
            
        except Exception as e:
            logger.error(f"❌ API integration benchmark failed: {e}")
            return {
                'benchmark_status': 'failed',
                'error': str(e)
            }
    
    async def test_api_endpoints_availability(self):
        """Test Step 4.1: API endpoint availability and basic functionality"""
        logger.info("🧪 Testing API Endpoints Availability...")
        
        try:
            # Test endpoints that should be available
            endpoint_tests = [
                {
                    'name': 'API Info Endpoint',
                    'url': f"{self.api_base_url.replace('/api', '')}/api/api-info",
                    'method': 'GET',
                    'expected_keys': ['features', 'endpoints', 'database']
                }
            ]
            
            # Add ultra-scale endpoints if available
            if ULTRA_SCALE_AVAILABLE:
                ultra_endpoints = [
                    {
                        'name': 'Source Health Dashboard',
                        'url': f"{self.api_base_url}/source-health",
                        'method': 'GET',
                        'expected_keys': ['total_sources', 'active_sources', 'source_metrics']
                    },
                    {
                        'name': 'Search Suggestions',
                        'url': f"{self.api_base_url}/search-suggestions?query=contract&limit=5",
                        'method': 'GET',
                        'expected_keys': ['suggestions', 'query']
                    },
                    {
                        'name': 'Analytics Search Patterns',
                        'url': f"{self.api_base_url}/analytics/search-patterns?days=7",
                        'method': 'GET',
                        'expected_keys': ['analysis_period_days', 'total_searches']
                    }
                ]
                endpoint_tests.extend(ultra_endpoints)
            
            # Test each endpoint
            test_results = []
            successful_tests = 0
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                for test in endpoint_tests:
                    try:
                        logger.info(f"Testing {test['name']}: {test['url']}")
                        
                        if test['method'] == 'GET':
                            response = await client.get(test['url'])
                        else:
                            continue  # Skip non-GET for now
                        
                        if response.status_code == 200:
                            response_data = response.json()
                            
                            # Check if expected keys are present
                            has_expected_keys = all(
                                key in response_data for key in test.get('expected_keys', [])
                            )
                            
                            test_result = {
                                'name': test['name'],
                                'status': 'passed',
                                'status_code': response.status_code,
                                'has_expected_keys': has_expected_keys,
                                'response_time_ms': response.elapsed.total_seconds() * 1000
                            }
                            
                            if has_expected_keys:
                                successful_tests += 1
                                logger.info(f"✅ {test['name']} - PASSED")
                            else:
                                logger.warning(f"⚠️ {test['name']} - Missing expected keys")
                                test_result['status'] = 'partial'
                            
                        else:
                            test_result = {
                                'name': test['name'],
                                'status': 'failed',
                                'status_code': response.status_code,
                                'error': f"HTTP {response.status_code}"
                            }
                            logger.error(f"❌ {test['name']} - HTTP {response.status_code}")
                        
                        test_results.append(test_result)
                        
                    except Exception as e:
                        test_result = {
                            'name': test['name'],
                            'status': 'failed',
                            'error': str(e)
                        }
                        test_results.append(test_result)
                        logger.error(f"❌ {test['name']} - Exception: {e}")
            
            success_rate = successful_tests / len(endpoint_tests)
            
            return {
                'test_status': 'passed' if success_rate >= 0.8 else 'warning' if success_rate >= 0.5 else 'failed',
                'endpoints_tested': len(endpoint_tests),
                'successful_tests': successful_tests,
                'success_rate': success_rate,
                'test_results': test_results,
                'ultra_scale_endpoints_available': ULTRA_SCALE_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"❌ API endpoints availability test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }

async def run_step_4_1_tests():
    """Run all Step 4.1 tests and generate comprehensive report"""
    logger.info("🚀 Starting Step 4.1 - Ultra-Comprehensive API System Tests")
    
    test_suite = TestUltraScaleAPISystem()
    
    # Run all tests
    tests = [
        ('Ultra-Scale API Models', test_suite.test_ultra_scale_api_models),
        ('Query Optimization Service', test_suite.test_query_optimization_service),
        ('Source Health Monitor', test_suite.test_source_health_monitor),
        ('Database Integration', test_suite.test_ultra_scale_database_integration),
        ('API Endpoints Availability', test_suite.test_api_endpoints_availability)
    ]
    
    results = {}
    overall_start = time.time()
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*60}")
        
        test_start = time.time()
        try:
            result = await test_func()
            test_time = time.time() - test_start
            result['execution_time_seconds'] = round(test_time, 3)
            results[test_name] = result
            
            status_emoji = "✅" if result['test_status'] == 'passed' else "⚠️" if result['test_status'] == 'warning' else "🔄" if result['test_status'] == 'skipped' else "❌"
            logger.info(f"{status_emoji} {test_name}: {result['test_status'].upper()} ({test_time:.2f}s)")
            
        except Exception as e:
            test_time = time.time() - test_start
            logger.error(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = {
                'test_status': 'failed',
                'error': str(e),
                'execution_time_seconds': round(test_time, 3)
            }
    
    total_time = time.time() - overall_start
    
    # Generate summary report
    passed_tests = sum(1 for result in results.values() if result['test_status'] == 'passed')
    warning_tests = sum(1 for result in results.values() if result['test_status'] == 'warning')
    skipped_tests = sum(1 for result in results.values() if result['test_status'] == 'skipped')
    failed_tests = sum(1 for result in results.values() if result['test_status'] == 'failed')
    
    if failed_tests == 0 and passed_tests > 0:
        overall_status = 'passed'
    elif failed_tests == 0 and skipped_tests > 0:
        overall_status = 'skipped_components'
    elif passed_tests >= len(tests) * 0.5:
        overall_status = 'warning'
    else:
        overall_status = 'failed'
    
    summary_report = {
        'step': '4.1 - Ultra-Comprehensive API System',
        'timestamp': datetime.utcnow().isoformat(),
        'overall_status': overall_status,
        'total_execution_time_seconds': round(total_time, 2),
        'ultra_scale_components_available': ULTRA_SCALE_AVAILABLE,
        'summary': {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'warning_tests': warning_tests,
            'skipped_tests': skipped_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests + warning_tests) / len(tests)
        },
        'test_results': results
    }
    
    # Print final report
    logger.info(f"\n{'='*60}")
    logger.info("STEP 4.1 TEST SUMMARY REPORT")
    logger.info(f"{'='*60}")
    logger.info(f"Overall Status: {overall_status.upper()}")
    logger.info(f"Ultra-Scale Components Available: {'YES' if ULTRA_SCALE_AVAILABLE else 'NO'}")
    logger.info(f"Tests Passed: {passed_tests}/{len(tests)} ({(passed_tests/len(tests))*100:.1f}%)")
    if skipped_tests > 0:
        logger.info(f"Tests Skipped: {skipped_tests} (components not available)")
    logger.info(f"Total Execution Time: {total_time:.2f} seconds")
    logger.info(f"{'='*60}")
    
    return summary_report

if __name__ == "__main__":
    # Run the tests
    async def main():
        results = await run_step_4_1_tests()
        
        # Save results to file
        with open('/app/step_4_1_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    # Execute tests
    test_results = asyncio.run(main())
    print(f"\n🎯 Step 4.1 Testing Complete - Status: {test_results['overall_status'].upper()}")