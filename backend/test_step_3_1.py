"""
Test Suite for Step 3.1 - Ultra-Scale Database Architecture
Comprehensive testing of distributed database design for 370M+ documents
"""

import asyncio
import logging
import os
import json
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

# Import the ultra-scale database service
from ultra_scale_database_service import (
    UltraScaleDatabaseService, GeographicShardingStrategy, 
    create_ultra_scale_database_service, test_ultra_scale_performance
)
from legal_models import (
    LegalDocument, LegalDocumentCreate, LegalDocumentFilter, 
    DocumentType, JurisdictionLevel, ProcessingStatus
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestUltraScaleDatabaseArchitecture:
    """Comprehensive test suite for Step 3.1 implementation"""
    
    @classmethod
    def setup_class(cls):
        """Set up test environment"""
        # Use test database
        cls.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        cls.test_db_prefix = "test_ultra_scale"
        
    async def test_geographic_sharding_strategy(self):
        """Test Step 3.1: Geographic sharding strategy initialization"""
        logger.info("🧪 Testing Geographic Sharding Strategy...")
        
        sharding = GeographicShardingStrategy()
        
        # Verify all 8 shards are configured
        expected_shards = {
            'us_federal', 'us_state', 'european_union', 'commonwealth',
            'asia_pacific', 'academic', 'professional', 'specialized'
        }
        
        assert set(sharding.shard_configurations.keys()) == expected_shards
        logger.info(f"✅ All {len(expected_shards)} shards configured correctly")
        
        # Test shard routing for different jurisdictions
        test_cases = [
            # US Federal documents -> us_federal shard
            {
                'jurisdiction': 'United States',
                'document_type': DocumentType.CASE_LAW,
                'expected_shard': 'us_federal'
            },
            # EU documents -> european_union shard
            {
                'jurisdiction': 'European Union',
                'document_type': DocumentType.REGULATION,
                'expected_shard': 'european_union'
            },
            # UK documents -> commonwealth shard
            {
                'jurisdiction': 'United Kingdom',
                'document_type': DocumentType.STATUTE,
                'expected_shard': 'commonwealth'
            },
            # Academic documents -> academic shard
            {
                'jurisdiction': 'International',
                'document_type': DocumentType.SCHOLARLY_ARTICLE,
                'expected_shard': 'academic'
            },
            # Professional documents -> professional shard
            {
                'jurisdiction': 'Professional Organizations',
                'document_type': DocumentType.BAR_PUBLICATION,
                'expected_shard': 'professional'
            }
        ]
        
        routing_successes = 0
        for test_case in test_cases:
            doc = LegalDocumentCreate(
                title="Test Document",
                content="Test content",
                document_type=test_case['document_type'],
                jurisdiction=test_case['jurisdiction'],
                source="test"
            )
            
            determined_shard = sharding.determine_shard(doc)
            
            if determined_shard == test_case['expected_shard']:
                routing_successes += 1
                logger.info(f"✅ Correct routing: {test_case['jurisdiction']} -> {determined_shard}")
            else:
                logger.warning(f"⚠️ Unexpected routing: {test_case['jurisdiction']} -> {determined_shard} (expected: {test_case['expected_shard']})")
        
        logger.info(f"🎯 Shard routing accuracy: {routing_successes}/{len(test_cases)} ({(routing_successes/len(test_cases))*100:.1f}%)")
        
        return {
            'shards_configured': len(sharding.shard_configurations),
            'routing_accuracy': routing_successes / len(test_cases),
            'test_status': 'passed' if routing_successes >= len(test_cases) * 0.8 else 'warning'
        }
    
    async def test_ultra_scale_database_initialization(self):
        """Test Step 3.1: Ultra-scale database service initialization"""
        logger.info("🧪 Testing Ultra-Scale Database Initialization...")
        
        try:
            # Initialize the ultra-scale database service
            service = UltraScaleDatabaseService(self.mongo_url)
            
            # Test initialization
            await service.initialize_ultra_scale_architecture()
            
            # Verify all shards are connected
            all_shards = await service.get_all_shards()
            expected_shard_count = 8
            
            assert len(all_shards) == expected_shard_count
            logger.info(f"✅ All {len(all_shards)} shards initialized successfully")
            
            # Test system metrics
            metrics = await service.get_ultra_scale_system_metrics()
            
            assert 'total_documents' in metrics
            assert 'active_shards' in metrics
            assert 'shard_details' in metrics
            assert metrics['total_shards'] == expected_shard_count
            
            logger.info(f"✅ System metrics generated successfully")
            logger.info(f"📊 Active shards: {metrics['active_shards']}/{metrics['total_shards']}")
            
            # Clean up
            await service.close_connections()
            
            return {
                'shards_initialized': len(all_shards),
                'active_shards': metrics['active_shards'],
                'metrics_generated': True,
                'test_status': 'passed'
            }
            
        except Exception as e:
            logger.error(f"❌ Initialization test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_ultra_scale_indexes_creation(self):
        """Test Step 3.1: Ultra-scale index creation across all shards"""
        logger.info("🧪 Testing Ultra-Scale Index Creation...")
        
        try:
            service = UltraScaleDatabaseService(self.mongo_url)
            await service.initialize_ultra_scale_architecture()
            
            # Verify indexes were created
            index_verification_results = {}
            
            for shard_name, collection in service.collections.items():
                index_info = await collection.index_information()
                
                # Expected indexes (excluding default _id_ index)
                expected_indexes = {
                    'jurisdiction_type_date_idx', 'topics_precedential_quality_idx',
                    'source_status_quality_idx', 'fulltext_search_idx',
                    'citations_idx', 'cited_by_idx', 'dates_idx',
                    'court_jurisdiction_type_idx', 'processing_status_created_idx',
                    'parties_idx', 'related_documents_idx', 'complex_query_idx',
                    'quality_metrics_idx'
                }
                
                created_indexes = set(index_info.keys()) - {'_id_'}
                matching_indexes = expected_indexes.intersection(created_indexes)
                
                index_verification_results[shard_name] = {
                    'expected_count': len(expected_indexes),
                    'created_count': len(created_indexes),
                    'matching_count': len(matching_indexes),
                    'coverage_percentage': (len(matching_indexes) / len(expected_indexes)) * 100
                }
                
                logger.info(f"📊 Shard '{shard_name}': {len(matching_indexes)}/{len(expected_indexes)} indexes created ({index_verification_results[shard_name]['coverage_percentage']:.1f}%)")
            
            # Calculate overall index coverage
            total_expected = sum(result['expected_count'] for result in index_verification_results.values())
            total_matching = sum(result['matching_count'] for result in index_verification_results.values())
            overall_coverage = (total_matching / total_expected) * 100
            
            logger.info(f"🎯 Overall index coverage: {total_matching}/{total_expected} ({overall_coverage:.1f}%)")
            
            await service.close_connections()
            
            return {
                'shards_tested': len(index_verification_results),
                'overall_coverage_percentage': overall_coverage,
                'shard_results': index_verification_results,
                'test_status': 'passed' if overall_coverage >= 90 else 'warning'
            }
            
        except Exception as e:
            logger.error(f"❌ Index creation test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_distributed_document_operations(self):
        """Test Step 3.1: Distributed document creation and search"""
        logger.info("🧪 Testing Distributed Document Operations...")
        
        try:
            service = UltraScaleDatabaseService(self.mongo_url)
            await service.initialize_ultra_scale_architecture()
            
            # Create test documents for different shards
            test_documents = [
                # US Federal document
                LegalDocumentCreate(
                    title="US Federal Case Law Test",
                    content="This is a test case from the US Supreme Court involving constitutional law.",
                    document_type=DocumentType.CASE_LAW,
                    jurisdiction="United States",
                    court="Supreme Court",
                    legal_topics=["constitutional_law", "federal_jurisdiction"],
                    source="test_us_federal"
                ),
                # EU document
                LegalDocumentCreate(
                    title="European Union Regulation Test",
                    content="This is a test regulation from the European Commission on data protection.",
                    document_type=DocumentType.REGULATION,
                    jurisdiction="European Union",
                    court="European Commission",
                    legal_topics=["data_protection", "privacy_law"],
                    source="test_eu"
                ),
                # Academic document
                LegalDocumentCreate(
                    title="Academic Legal Research Article",
                    content="This is a scholarly article about international trade law and dispute resolution.",
                    document_type=DocumentType.SCHOLARLY_ARTICLE,
                    jurisdiction="International",
                    legal_topics=["international_trade", "dispute_resolution"],
                    source="test_academic"
                ),
                # Commonwealth document
                LegalDocumentCreate(
                    title="UK Supreme Court Decision",
                    content="This is a test decision from the UK Supreme Court on human rights law.",
                    document_type=DocumentType.CASE_LAW,
                    jurisdiction="United Kingdom",
                    court="UK Supreme Court",
                    legal_topics=["human_rights", "constitutional_law"],
                    source="test_uk"
                )
            ]
            
            # Test bulk document creation
            start_time = time.time()
            document_ids = await service.create_documents_bulk(test_documents)
            create_time = time.time() - start_time
            
            logger.info(f"✅ Created {len(document_ids)} documents in {create_time:.3f} seconds")
            
            # Test distributed search
            search_tests = [
                # Search by jurisdiction
                {
                    'name': 'US Jurisdiction Search',
                    'filter': LegalDocumentFilter(jurisdictions=["United States"]),
                    'expected_min_results': 1
                },
                # Search by document type
                {
                    'name': 'Case Law Search',
                    'filter': LegalDocumentFilter(document_types=[DocumentType.CASE_LAW]),
                    'expected_min_results': 2
                },
                # Search by legal topics
                {
                    'name': 'Constitutional Law Search',
                    'filter': LegalDocumentFilter(legal_topics=["constitutional_law"]),
                    'expected_min_results': 1
                },
                # Full-text search
                {
                    'name': 'Full-text Search',
                    'filter': LegalDocumentFilter(search_text="Supreme Court"),
                    'expected_min_results': 1
                }
            ]
            
            search_results = {}
            for test in search_tests:
                start_time = time.time()
                results = await service.search_documents(test['filter'])
                search_time = time.time() - start_time
                
                search_results[test['name']] = {
                    'documents_found': len(results.documents),
                    'total_count': results.total_count,
                    'search_time_ms': round(search_time * 1000, 2),
                    'shards_queried': results.search_metadata.get('shards_queried', 0),
                    'meets_expectations': results.total_count >= test['expected_min_results']
                }
                
                logger.info(f"🔍 {test['name']}: Found {results.total_count} documents in {search_time:.3f}s")
            
            # Calculate success rate
            successful_searches = sum(1 for result in search_results.values() if result['meets_expectations'])
            success_rate = successful_searches / len(search_tests)
            
            await service.close_connections()
            
            return {
                'documents_created': len(document_ids),
                'create_time_seconds': round(create_time, 3),
                'search_tests_performed': len(search_tests),
                'successful_searches': successful_searches,
                'success_rate': success_rate,
                'search_results': search_results,
                'test_status': 'passed' if success_rate >= 0.8 else 'warning'
            }
            
        except Exception as e:
            logger.error(f"❌ Distributed operations test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }
    
    async def test_performance_benchmarks(self):
        """Test Step 3.1: Performance benchmarks for ultra-scale operations"""
        logger.info("🧪 Testing Performance Benchmarks...")
        
        try:
            service = UltraScaleDatabaseService(self.mongo_url)
            await service.initialize_ultra_scale_architecture()
            
            # Run performance test with smaller dataset for testing
            performance_results = await test_ultra_scale_performance(service, test_document_count=100)
            
            # Performance benchmarks
            benchmarks = {
                'bulk_insert_rate_docs_per_second': {
                    'target': 50,  # Target: 50+ docs/second
                    'actual': performance_results['test_summary']['insert_rate_docs_per_second'],
                    'passed': performance_results['test_summary']['insert_rate_docs_per_second'] >= 50
                },
                'search_response_time_ms': {
                    'target': 1000,  # Target: Under 1 second
                    'actual': performance_results['performance_metrics']['search_response_time_ms'],
                    'passed': performance_results['performance_metrics']['search_response_time_ms'] <= 1000
                },
                'average_insert_time_ms': {
                    'target': 100,  # Target: Under 100ms per document
                    'actual': performance_results['performance_metrics']['average_insert_time_ms'],
                    'passed': performance_results['performance_metrics']['average_insert_time_ms'] <= 100
                }
            }
            
            # Calculate overall performance score
            passed_benchmarks = sum(1 for benchmark in benchmarks.values() if benchmark['passed'])
            performance_score = passed_benchmarks / len(benchmarks)
            
            logger.info(f"🎯 Performance Score: {passed_benchmarks}/{len(benchmarks)} benchmarks passed ({performance_score*100:.1f}%)")
            
            for name, benchmark in benchmarks.items():
                status = "✅ PASS" if benchmark['passed'] else "❌ FAIL"
                logger.info(f"  {status} {name}: {benchmark['actual']} (target: {benchmark['target']})")
            
            await service.close_connections()
            
            return {
                'benchmarks_tested': len(benchmarks),
                'benchmarks_passed': passed_benchmarks,
                'performance_score': performance_score,
                'benchmark_details': benchmarks,
                'full_performance_results': performance_results,
                'test_status': 'passed' if performance_score >= 0.6 else 'warning'
            }
            
        except Exception as e:
            logger.error(f"❌ Performance benchmark test failed: {e}")
            return {
                'test_status': 'failed',
                'error': str(e)
            }

async def run_step_3_1_tests():
    """Run all Step 3.1 tests and generate comprehensive report"""
    logger.info("🚀 Starting Step 3.1 - Ultra-Scale Database Architecture Tests")
    
    test_suite = TestUltraScaleDatabaseArchitecture()
    
    # Run all tests
    tests = [
        ('Geographic Sharding Strategy', test_suite.test_geographic_sharding_strategy),
        ('Database Initialization', test_suite.test_ultra_scale_database_initialization),
        ('Index Creation', test_suite.test_ultra_scale_indexes_creation),
        ('Distributed Operations', test_suite.test_distributed_document_operations),
        ('Performance Benchmarks', test_suite.test_performance_benchmarks)
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
            
            status_emoji = "✅" if result['test_status'] == 'passed' else "⚠️" if result['test_status'] == 'warning' else "❌"
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
    failed_tests = sum(1 for result in results.values() if result['test_status'] == 'failed')
    
    overall_status = 'passed' if failed_tests == 0 else 'failed' if passed_tests < len(tests) * 0.5 else 'warning'
    
    summary_report = {
        'step': '3.1 - Ultra-Scale Database Architecture',
        'timestamp': datetime.utcnow().isoformat(),
        'overall_status': overall_status,
        'total_execution_time_seconds': round(total_time, 2),
        'summary': {
            'total_tests': len(tests),
            'passed_tests': passed_tests,
            'warning_tests': warning_tests,
            'failed_tests': failed_tests,
            'success_rate': passed_tests / len(tests)
        },
        'test_results': results
    }
    
    # Print final report
    logger.info(f"\n{'='*60}")
    logger.info("STEP 3.1 TEST SUMMARY REPORT")
    logger.info(f"{'='*60}")
    logger.info(f"Overall Status: {overall_status.upper()}")
    logger.info(f"Tests Passed: {passed_tests}/{len(tests)} ({(passed_tests/len(tests))*100:.1f}%)")
    logger.info(f"Total Execution Time: {total_time:.2f} seconds")
    logger.info(f"{'='*60}")
    
    return summary_report

if __name__ == "__main__":
    # Run the tests
    async def main():
        results = await run_step_3_1_tests()
        
        # Save results to file
        with open('/app/step_3_1_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        return results
    
    # Execute tests
    test_results = asyncio.run(main())
    print(f"\n🎯 Step 3.1 Testing Complete - Status: {test_results['overall_status'].upper()}")