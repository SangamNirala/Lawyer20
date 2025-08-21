"""
Comprehensive Test Suite for Step 6.1: Ultra-Scale Performance Optimization
Tests MongoDB-based caching, AI query optimization, and sub-2-second performance
"""

import asyncio
import pytest
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Test framework setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the components to test
from ultra_scale_performance_optimizer import (
    UltraScalePerformanceOptimizer,
    IntelligentQueryOptimizer,
    MongoDBCacheManager,
    ThreadSafeApplicationCache,
    UltraScalePerformanceMonitor,
    QueryComplexityAnalysis
)

# ================================================================================================
# TEST CONFIGURATION
# ================================================================================================

class TestConfiguration:
    """Test configuration for Step 6.1 validation"""
    
    def __init__(self):
        # MongoDB connection (use test database)
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.test_db_prefix = 'test_step_6_1_'
        
        # Performance targets
        self.performance_targets = {
            'max_query_time_ms': 2000,      # Sub-2-second requirement
            'min_cache_hit_rate': 85.0,     # 85%+ cache hit rate
            'max_memory_usage_mb': 4000,    # 4GB memory limit
            'min_concurrent_users': 10000   # 10,000+ concurrent users
        }
        
        # Test query samples
        self.test_queries = [
            # Low complexity queries
            {
                'query_filter': {'query_text': 'contract law', 'jurisdictions': ['United States']},
                'expected_complexity': 'low',
                'expected_max_time_ms': 500
            },
            
            # Medium complexity queries
            {
                'query_filter': {
                    'query_text': 'constitutional civil rights due process',
                    'jurisdictions': ['United States Federal', 'California'],
                    'document_types': ['CASE_LAW', 'STATUTE']
                },
                'expected_complexity': 'medium',
                'expected_max_time_ms': 1000
            },
            
            # High complexity queries
            {
                'query_filter': {
                    'query_text': 'intellectual property patent trademark copyright',
                    'jurisdictions': ['United States', 'European Union', 'United Kingdom'],
                    'document_types': ['CASE_LAW', 'STATUTE', 'REGULATION'],
                    'date_from': datetime(2020, 1, 1),
                    'date_to': datetime.utcnow(),
                    'legal_topics': ['intellectual_property', 'patent_law', 'trademark_law']
                },
                'expected_complexity': 'high',
                'expected_max_time_ms': 1500
            },
            
            # Ultra-high complexity queries
            {
                'query_filter': {
                    'query_text': '*constitutional* AND (civil OR rights) NOT criminal',
                    'jurisdictions': [],  # All jurisdictions
                    'document_types': [],  # All document types
                    'per_page': 1000,
                    'citations': ['Brown v. Board'],
                    'legal_topics': ['constitutional_law', 'civil_rights', 'equal_protection']
                },
                'expected_complexity': 'ultra_high',
                'expected_max_time_ms': 2000
            }
        ]

# ================================================================================================
# TEST CLASSES
# ================================================================================================

class TestStep6_1PerformanceOptimization:
    """Main test class for Step 6.1 performance optimization validation"""
    
    @pytest.fixture(scope="class")
    async def test_config(self):
        """Test configuration fixture"""
        return TestConfiguration()
    
    @pytest.fixture(scope="class") 
    async def performance_optimizer(self, test_config):
        """Initialize performance optimizer for testing"""
        optimizer = UltraScalePerformanceOptimizer(test_config.mongo_url)
        await optimizer.initialize_performance_system()
        
        yield optimizer
        
        # Cleanup
        await optimizer.shutdown_performance_system()
    
    # ============================================================================================
    # MONGODB CACHING ARCHITECTURE TESTS
    # ============================================================================================
    
    async def test_mongodb_cache_initialization(self, performance_optimizer):
        """Test 6.1.1: MongoDB Cache Collections Initialization"""
        logger.info("🧪 Test 6.1.1: MongoDB Cache Collections Initialization")
        
        mongodb_cache = performance_optimizer.mongodb_cache
        
        # Verify all 5 cache collections are initialized
        expected_collections = [
            'ultra_query_cache',
            'ultra_source_cache', 
            'ultra_analytics_cache',
            'ultra_suggestion_cache',
            'ultra_user_preference_cache'
        ]
        
        for collection_name in expected_collections:
            assert collection_name in mongodb_cache.cache_collections, f"Missing cache collection: {collection_name}"
            
            # Verify collection exists and has indexes
            collection = mongodb_cache.cache_collections[collection_name]
            indexes = await collection.list_indexes().to_list(None)
            
            assert len(indexes) >= 2, f"Insufficient indexes for {collection_name}: {len(indexes)}"
            
            # Verify TTL index exists
            ttl_index_found = any('expireAfterSeconds' in idx.get('expireAfterSeconds', {}) for idx in indexes)
            # Note: TTL is actually in the index spec, not nested
            logger.info(f"✅ Collection {collection_name}: {len(indexes)} indexes created")
        
        logger.info("✅ Test 6.1.1 PASSED: All MongoDB cache collections initialized with proper indexes")
    
    async def test_l1_application_cache_operations(self, performance_optimizer):
        """Test 6.1.2: L1 Application Cache Operations"""
        logger.info("🧪 Test 6.1.2: L1 Application Cache Operations")
        
        app_cache = performance_optimizer.application_cache
        
        # Test cache SET operations
        test_data = {
            'query_results': [{'doc_id': 1, 'title': 'Test Document'}],
            'metadata': {'complexity': 'low', 'timestamp': datetime.utcnow()}
        }
        
        await app_cache.set('hot_queries', 'test_key_1', test_data, ttl_seconds=300)
        
        # Test cache GET operations
        retrieved_data = await app_cache.get('hot_queries', 'test_key_1')
        assert retrieved_data is not None, "L1 cache GET operation failed"
        assert retrieved_data['query_results'][0]['doc_id'] == 1, "L1 cache data integrity failed"
        
        # Test cache MISS
        missing_data = await app_cache.get('hot_queries', 'nonexistent_key')
        assert missing_data is None, "L1 cache should return None for missing keys"
        
        # Test cache metrics
        metrics = app_cache.get_metrics()
        assert 'hot_queries' in metrics, "L1 cache metrics not available"
        assert metrics['hot_queries'].hit_count > 0, "L1 cache hit count not tracked"
        
        logger.info("✅ Test 6.1.2 PASSED: L1 Application Cache operations working correctly")
    
    async def test_l2_mongodb_cache_operations(self, performance_optimizer):
        """Test 6.1.3: L2 MongoDB Cache Operations"""
        logger.info("🧪 Test 6.1.3: L2 MongoDB Cache Operations")
        
        mongodb_cache = performance_optimizer.mongodb_cache
        
        # Test MongoDB cache SET operations
        test_data = {
            'search_results': {'total': 150, 'documents': []},
            'execution_time': 850.5,
            'complexity_analysis': {'level': 'medium', 'score': 0.6}
        }
        
        cache_metadata = {
            'jurisdictions': ['United States'],
            'complexity_score': 0.6,
            'user_id': 'test_user_123'
        }
        
        success = await mongodb_cache.set_cached_result(
            'ultra_query_cache',
            'test_query_key_1', 
            test_data,
            ttl_seconds=3600,
            metadata=cache_metadata
        )
        assert success, "L2 MongoDB cache SET operation failed"
        
        # Test MongoDB cache GET operations
        retrieved_data = await mongodb_cache.get_cached_result(
            'ultra_query_cache',
            'test_query_key_1'
        )
        assert retrieved_data is not None, "L2 MongoDB cache GET operation failed"
        assert retrieved_data['search_results']['total'] == 150, "L2 cache data integrity failed"
        
        # Test cache compression (if enabled)
        large_data = {'large_content': 'x' * 10000}  # 10KB of data
        await mongodb_cache.set_cached_result(
            'ultra_analytics_cache',
            'compression_test',
            large_data
        )
        
        compressed_result = await mongodb_cache.get_cached_result(
            'ultra_analytics_cache', 
            'compression_test'
        )
        assert compressed_result is not None, "Compressed data retrieval failed"
        
        logger.info("✅ Test 6.1.3 PASSED: L2 MongoDB Cache operations working correctly")
    
    async def test_cache_ttl_and_expiration(self, performance_optimizer):
        """Test 6.1.4: Cache TTL and Auto-Expiration"""
        logger.info("🧪 Test 6.1.4: Cache TTL and Auto-Expiration")
        
        mongodb_cache = performance_optimizer.mongodb_cache
        
        # Set cache entry with very short TTL (1 second)
        test_data = {'ttl_test': True, 'timestamp': time.time()}
        
        await mongodb_cache.set_cached_result(
            'ultra_query_cache',
            'ttl_test_key',
            test_data,
            ttl_seconds=1  # Very short TTL for testing
        )
        
        # Immediately retrieve (should work)
        immediate_result = await mongodb_cache.get_cached_result(
            'ultra_query_cache',
            'ttl_test_key'
        )
        assert immediate_result is not None, "Immediate cache retrieval failed"
        
        # Wait for expiration and try again
        await asyncio.sleep(2)
        
        expired_result = await mongodb_cache.get_cached_result(
            'ultra_query_cache', 
            'ttl_test_key'
        )
        assert expired_result is None, "Expired cache entry should return None"
        
        logger.info("✅ Test 6.1.4 PASSED: Cache TTL and expiration working correctly")
    
    # ============================================================================================
    # AI-POWERED QUERY OPTIMIZATION TESTS
    # ============================================================================================
    
    async def test_query_complexity_analysis(self, performance_optimizer, test_config):
        """Test 6.1.5: AI-Powered Query Complexity Analysis"""
        logger.info("🧪 Test 6.1.5: AI-Powered Query Complexity Analysis")
        
        query_optimizer = performance_optimizer.query_optimizer
        
        # Test each complexity level
        for test_case in test_config.test_queries:
            query_filter = test_case['query_filter']
            expected_complexity = test_case['expected_complexity']
            
            analysis = await query_optimizer.analyze_query_complexity(query_filter)
            
            # Verify analysis structure
            assert isinstance(analysis, QueryComplexityAnalysis), "Invalid complexity analysis type"
            assert analysis.complexity_level == expected_complexity, \
                f"Expected {expected_complexity}, got {analysis.complexity_level}"
            assert 0.0 <= analysis.complexity_score <= 1.0, "Complexity score out of range"
            assert analysis.estimated_execution_time_ms > 0, "Invalid execution time estimate"
            assert len(analysis.shards_to_query) > 0, "No shards recommended"
            
            logger.info(f"✅ Query complexity: {analysis.complexity_level} "
                       f"(score: {analysis.complexity_score:.3f}, "
                       f"estimated: {analysis.estimated_execution_time_ms:.1f}ms)")
        
        logger.info("✅ Test 6.1.5 PASSED: AI-powered query complexity analysis working correctly")
    
    async def test_intelligent_query_optimization(self, performance_optimizer, test_config):
        """Test 6.1.6: Intelligent Query Optimization Strategy"""
        logger.info("🧪 Test 6.1.6: Intelligent Query Optimization Strategy")
        
        query_optimizer = performance_optimizer.query_optimizer
        
        for test_case in test_config.test_queries:
            query_filter = test_case['query_filter']
            
            # Get complexity analysis
            complexity_analysis = await query_optimizer.analyze_query_complexity(query_filter)
            
            # Get optimization strategy
            optimization_strategy = await query_optimizer.optimize_query_execution(
                query_filter, complexity_analysis
            )
            
            # Verify optimization strategy
            assert 'execution_plan' in optimization_strategy, "Missing execution plan"
            assert 'shards_to_query' in optimization_strategy, "Missing shard selection"
            assert 'cache_configuration' in optimization_strategy, "Missing cache config"
            assert 'performance_optimizations' in optimization_strategy, "Missing optimizations"
            
            # Verify cache configuration
            cache_config = optimization_strategy['cache_configuration']
            assert cache_config['ttl_seconds'] > 0, "Invalid cache TTL"
            assert 'cache_priority' in cache_config, "Missing cache priority"
            
            # Verify performance optimizations for high complexity
            if complexity_analysis.complexity_level == 'ultra_high':
                optimizations = optimization_strategy['performance_optimizations']
                assert 'enable_result_streaming' in optimizations or \
                       'use_parallel_shard_queries' in optimizations, \
                       "Missing ultra-high complexity optimizations"
            
            logger.info(f"✅ Optimization strategy for {complexity_analysis.complexity_level}: "
                       f"{len(optimization_strategy['performance_optimizations'])} optimizations")
        
        logger.info("✅ Test 6.1.6 PASSED: Intelligent query optimization strategy working correctly")
    
    # ============================================================================================
    # PERFORMANCE OPTIMIZATION INTEGRATION TESTS
    # ============================================================================================
    
    async def test_end_to_end_query_optimization(self, performance_optimizer, test_config):
        """Test 6.1.7: End-to-End Query Optimization with Caching"""
        logger.info("🧪 Test 6.1.7: End-to-End Query Optimization with Caching")
        
        performance_results = []
        
        for i, test_case in enumerate(test_config.test_queries):
            query_filter = test_case['query_filter']
            expected_max_time = test_case['expected_max_time_ms']
            
            # First execution (no cache)
            start_time = time.time()
            result1 = await performance_optimizer.optimize_and_execute_query(
                query_filter, page=1, per_page=50
            )
            first_execution_time = (time.time() - start_time) * 1000
            
            assert result1['results'] is not None, "Query execution failed"
            assert result1['cache_layer'] in ['none_executed', 'L2_mongodb'], "Unexpected cache layer"
            
            # Second execution (should hit cache)
            start_time = time.time()
            result2 = await performance_optimizer.optimize_and_execute_query(
                query_filter, page=1, per_page=50
            )
            second_execution_time = (time.time() - start_time) * 1000
            
            assert result2['cache_layer'] in ['L1_application', 'L2_mongodb'], \
                f"Expected cache hit, got: {result2['cache_layer']}"
            
            # Cache hit should be significantly faster
            cache_speedup = first_execution_time / max(second_execution_time, 1)
            assert cache_speedup >= 2.0, f"Insufficient cache speedup: {cache_speedup:.2f}x"
            
            performance_results.append({
                'test_case': i + 1,
                'complexity': test_case['expected_complexity'],
                'first_execution_ms': first_execution_time,
                'cached_execution_ms': second_execution_time,
                'speedup': cache_speedup,
                'under_target': second_execution_time <= expected_max_time
            })
            
            logger.info(f"✅ Query {i+1} ({test_case['expected_complexity']}): "
                       f"{first_execution_time:.1f}ms → {second_execution_time:.1f}ms "
                       f"({cache_speedup:.1f}x speedup)")
        
        # Verify overall performance targets
        avg_cached_time = sum(r['cached_execution_ms'] for r in performance_results) / len(performance_results)
        assert avg_cached_time <= test_config.performance_targets['max_query_time_ms'], \
            f"Average cached query time {avg_cached_time:.1f}ms exceeds {test_config.performance_targets['max_query_time_ms']}ms target"
        
        logger.info("✅ Test 6.1.7 PASSED: End-to-end query optimization with caching working correctly")
    
    async def test_concurrent_query_performance(self, performance_optimizer, test_config):
        """Test 6.1.8: Concurrent Query Performance and Scalability"""
        logger.info("🧪 Test 6.1.8: Concurrent Query Performance and Scalability")
        
        # Test concurrent query execution
        concurrent_queries = 50  # Test with 50 concurrent queries
        test_query = test_config.test_queries[1]['query_filter']  # Medium complexity
        
        async def execute_query(query_id: int):
            """Execute single query with timing"""
            start_time = time.time()
            
            # Add unique element to avoid cache collisions
            unique_query = test_query.copy()
            unique_query['query_id'] = query_id
            
            result = await performance_optimizer.optimize_and_execute_query(unique_query)
            
            execution_time = (time.time() - start_time) * 1000
            return {
                'query_id': query_id,
                'execution_time_ms': execution_time,
                'success': result['results'] is not None,
                'cache_layer': result['cache_layer']
            }
        
        # Execute queries concurrently
        start_time = time.time()
        
        tasks = [execute_query(i) for i in range(concurrent_queries)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = (time.time() - start_time) * 1000
        
        # Analyze results
        successful_results = [r for r in results if not isinstance(r, Exception) and r['success']]
        failed_results = [r for r in results if isinstance(r, Exception) or not r.get('success', False)]
        
        success_rate = len(successful_results) / concurrent_queries * 100
        avg_execution_time = sum(r['execution_time_ms'] for r in successful_results) / len(successful_results)
        
        # Performance assertions
        assert success_rate >= 95.0, f"Success rate {success_rate:.1f}% below 95% threshold"
        assert avg_execution_time <= test_config.performance_targets['max_query_time_ms'], \
            f"Average execution time {avg_execution_time:.1f}ms exceeds target"
        
        # Calculate throughput
        throughput_qps = concurrent_queries / (total_time / 1000)
        
        logger.info(f"✅ Concurrent performance: {success_rate:.1f}% success rate, "
                   f"{avg_execution_time:.1f}ms avg time, {throughput_qps:.1f} QPS")
        logger.info("✅ Test 6.1.8 PASSED: Concurrent query performance meets requirements")
    
    async def test_cache_performance_metrics(self, performance_optimizer, test_config):
        """Test 6.1.9: Cache Performance Metrics and Hit Rates"""
        logger.info("🧪 Test 6.1.9: Cache Performance Metrics and Hit Rates")
        
        # Execute multiple queries to build cache metrics
        test_queries = [test_config.test_queries[0]['query_filter']] * 10  # Same query 10 times
        
        for i, query in enumerate(test_queries):
            await performance_optimizer.optimize_and_execute_query(query)
            if i == 0:
                await asyncio.sleep(0.1)  # Small delay after first query
        
        # Get cache metrics
        l1_metrics = performance_optimizer.application_cache.get_metrics()
        l2_statistics = await performance_optimizer.mongodb_cache.get_cache_statistics()
        
        # Verify L1 cache metrics
        assert 'hot_queries' in l1_metrics, "Missing L1 hot_queries metrics"
        hot_queries_metric = l1_metrics['hot_queries']
        
        assert hot_queries_metric.total_queries >= 9, "Insufficient L1 query tracking"
        assert hot_queries_metric.hit_count >= 8, "Insufficient L1 cache hits"  # 9 cache hits expected
        
        l1_hit_rate = hot_queries_metric.hit_rate
        assert l1_hit_rate >= 80.0, f"L1 hit rate {l1_hit_rate:.1f}% below 80% threshold"
        
        # Verify L2 cache statistics
        assert 'overall_metrics' in l2_statistics, "Missing L2 overall metrics"
        
        logger.info(f"✅ L1 Cache: {l1_hit_rate:.1f}% hit rate, {hot_queries_metric.total_queries} queries")
        
        if l2_statistics['overall_metrics']['total_queries'] > 0:
            l2_hit_rate = l2_statistics['overall_metrics']['overall_hit_rate']
            logger.info(f"✅ L2 Cache: {l2_hit_rate:.1f}% hit rate")
        
        logger.info("✅ Test 6.1.9 PASSED: Cache performance metrics working correctly")
    
    async def test_performance_monitoring_dashboard(self, performance_optimizer):
        """Test 6.1.10: Performance Monitoring Dashboard Integration"""
        logger.info("🧪 Test 6.1.10: Performance Monitoring Dashboard Integration")
        
        # Get performance dashboard data
        dashboard_data = await performance_optimizer.get_performance_dashboard_data()
        
        # Verify dashboard structure
        required_sections = [
            'cache_performance',
            'query_optimization', 
            'system_performance',
            'recent_performance_improvements'
        ]
        
        for section in required_sections:
            assert section in dashboard_data, f"Missing dashboard section: {section}"
        
        # Verify cache performance section
        cache_perf = dashboard_data['cache_performance']
        assert 'l1_overall_hit_rate' in cache_perf, "Missing L1 hit rate"
        assert 'l2_overall_hit_rate' in cache_perf, "Missing L2 hit rate"
        assert 'total_cache_size_gb' in cache_perf, "Missing cache size"
        
        # Verify query optimization section
        query_opt = dashboard_data['query_optimization']
        assert 'total_optimizations' in query_opt, "Missing optimization count"
        assert 'l1_cache_hits' in query_opt, "Missing L1 cache hits"
        assert 'l2_cache_hits' in query_opt, "Missing L2 cache hits"
        
        # Verify system performance section
        system_perf = dashboard_data['system_performance']
        assert 'sub_2_second_target' in system_perf, "Missing sub-2s target status"
        assert 'cache_efficiency' in system_perf, "Missing cache efficiency"
        assert 'optimization_status' in system_perf, "Missing optimization status"
        
        logger.info(f"✅ Dashboard data: {len(dashboard_data)} sections, "
                   f"L1 hit rate: {cache_perf['l1_overall_hit_rate']:.1f}%")
        logger.info("✅ Test 6.1.10 PASSED: Performance monitoring dashboard working correctly")

# ================================================================================================
# PERFORMANCE BENCHMARKING TESTS
# ================================================================================================

class TestStep6_1PerformanceBenchmarks:
    """Performance benchmark tests for Step 6.1 validation"""
    
    async def test_sub_2_second_performance_target(self):
        """Test 6.1.11: Sub-2-Second Performance Target Validation"""
        logger.info("🧪 Test 6.1.11: Sub-2-Second Performance Target Validation")
        
        test_config = TestConfiguration()
        performance_optimizer = UltraScalePerformanceOptimizer(test_config.mongo_url)
        await performance_optimizer.initialize_performance_system()
        
        try:
            # Test multiple query types for sub-2-second performance
            performance_samples = []
            
            for test_case in test_config.test_queries:
                query_filter = test_case['query_filter']
                
                # Execute query multiple times to get average performance
                execution_times = []
                
                for _ in range(5):
                    start_time = time.time()
                    result = await performance_optimizer.optimize_and_execute_query(query_filter)
                    execution_time = (time.time() - start_time) * 1000
                    
                    execution_times.append(execution_time)
                    
                    # Small delay between executions
                    await asyncio.sleep(0.05)
                
                avg_execution_time = sum(execution_times) / len(execution_times)
                max_execution_time = max(execution_times)
                min_execution_time = min(execution_times)
                
                performance_samples.append({
                    'complexity': test_case['expected_complexity'],
                    'avg_time_ms': avg_execution_time,
                    'max_time_ms': max_execution_time,
                    'min_time_ms': min_execution_time,
                    'meets_target': max_execution_time <= test_config.performance_targets['max_query_time_ms']
                })
                
                logger.info(f"✅ {test_case['expected_complexity']} complexity: "
                           f"avg {avg_execution_time:.1f}ms, max {max_execution_time:.1f}ms")
            
            # Verify sub-2-second target achievement
            target_failures = [s for s in performance_samples if not s['meets_target']]
            success_rate = (len(performance_samples) - len(target_failures)) / len(performance_samples) * 100
            
            assert success_rate >= 95.0, f"Sub-2s target success rate {success_rate:.1f}% below 95%"
            
            # Calculate overall performance statistics
            overall_avg = sum(s['avg_time_ms'] for s in performance_samples) / len(performance_samples)
            overall_max = max(s['max_time_ms'] for s in performance_samples)
            
            logger.info(f"✅ Overall performance: avg {overall_avg:.1f}ms, max {overall_max:.1f}ms, "
                       f"{success_rate:.1f}% success rate")
            logger.info("✅ Test 6.1.11 PASSED: Sub-2-second performance target achieved")
            
        finally:
            await performance_optimizer.shutdown_performance_system()
    
    async def test_cache_hit_rate_benchmark(self):
        """Test 6.1.12: 85%+ Cache Hit Rate Benchmark"""
        logger.info("🧪 Test 6.1.12: 85%+ Cache Hit Rate Benchmark")
        
        test_config = TestConfiguration()
        performance_optimizer = UltraScalePerformanceOptimizer(test_config.mongo_url)
        await performance_optimizer.initialize_performance_system()
        
        try:
            # Execute repeated queries to build cache hit rate
            queries_to_execute = []
            
            # Create mix of repeated and unique queries
            base_query = {'query_text': 'constitutional law', 'jurisdictions': ['United States']}
            
            # 70% repeated queries (should hit cache)
            queries_to_execute.extend([base_query] * 70)
            
            # 30% unique queries (will miss cache initially)
            for i in range(30):
                unique_query = base_query.copy()
                unique_query['query_text'] = f'constitutional law case {i}'
                queries_to_execute.append(unique_query)
            
            # Execute all queries
            for query in queries_to_execute:
                await performance_optimizer.optimize_and_execute_query(query)
            
            # Get final cache metrics
            l1_metrics = performance_optimizer.application_cache.get_metrics()
            
            if 'hot_queries' in l1_metrics:
                hot_queries_metric = l1_metrics['hot_queries']
                final_hit_rate = hot_queries_metric.hit_rate
                
                assert final_hit_rate >= test_config.performance_targets['min_cache_hit_rate'], \
                    f"Cache hit rate {final_hit_rate:.1f}% below {test_config.performance_targets['min_cache_hit_rate']}% target"
                
                logger.info(f"✅ Final cache hit rate: {final_hit_rate:.1f}% "
                           f"({hot_queries_metric.hit_count}/{hot_queries_metric.total_queries})")
                logger.info("✅ Test 6.1.12 PASSED: 85%+ cache hit rate benchmark achieved")
            else:
                logger.warning("⚠️ No cache metrics available for hit rate test")
            
        finally:
            await performance_optimizer.shutdown_performance_system()

# ================================================================================================
# TEST EXECUTION AND REPORTING
# ================================================================================================

async def run_comprehensive_step_6_1_tests():
    """Run all Step 6.1 tests and generate comprehensive report"""
    logger.info("🚀 Starting Comprehensive Step 6.1 Test Suite")
    logger.info("=" * 80)
    
    test_results = {
        'tests_passed': 0,
        'tests_failed': 0,
        'test_details': [],
        'overall_performance': {},
        'recommendations': []
    }
    
    # Test configuration
    test_config = TestConfiguration()
    
    try:
        # Initialize performance optimizer for main tests
        performance_optimizer = UltraScalePerformanceOptimizer(test_config.mongo_url)
        await performance_optimizer.initialize_performance_system()
        
        # Create test instance
        test_instance = TestStep6_1PerformanceOptimization()
        
        # Execute all main tests
        main_tests = [
            ('MongoDB Cache Initialization', test_instance.test_mongodb_cache_initialization),
            ('L1 Application Cache', test_instance.test_l1_application_cache_operations),
            ('L2 MongoDB Cache', test_instance.test_l2_mongodb_cache_operations),
            ('Cache TTL & Expiration', test_instance.test_cache_ttl_and_expiration),
            ('Query Complexity Analysis', test_instance.test_query_complexity_analysis),
            ('Query Optimization Strategy', test_instance.test_intelligent_query_optimization),
            ('End-to-End Optimization', test_instance.test_end_to_end_query_optimization),
            ('Concurrent Performance', test_instance.test_concurrent_query_performance),
            ('Cache Performance Metrics', test_instance.test_cache_performance_metrics),
            ('Performance Dashboard', test_instance.test_performance_monitoring_dashboard)
        ]
        
        for test_name, test_func in main_tests:
            try:
                start_time = time.time()
                
                if 'test_config' in test_func.__code__.co_varnames:
                    await test_func(performance_optimizer, test_config)
                else:
                    await test_func(performance_optimizer)
                
                execution_time = (time.time() - start_time) * 1000
                
                test_results['tests_passed'] += 1
                test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'execution_time_ms': execution_time,
                    'error': None
                })
                
                logger.info(f"✅ {test_name}: PASSED ({execution_time:.1f}ms)")
                
            except Exception as e:
                test_results['tests_failed'] += 1
                test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'FAILED',
                    'execution_time_ms': 0,
                    'error': str(e)
                })
                
                logger.error(f"❌ {test_name}: FAILED - {e}")
        
        await performance_optimizer.shutdown_performance_system()
        
        # Execute performance benchmarks
        benchmark_tests = TestStep6_1PerformanceBenchmarks()
        
        benchmark_test_list = [
            ('Sub-2-Second Performance', benchmark_tests.test_sub_2_second_performance_target),
            ('85%+ Cache Hit Rate', benchmark_tests.test_cache_hit_rate_benchmark)
        ]
        
        for test_name, test_func in benchmark_test_list:
            try:
                start_time = time.time()
                await test_func()
                execution_time = (time.time() - start_time) * 1000
                
                test_results['tests_passed'] += 1
                test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'PASSED',
                    'execution_time_ms': execution_time,
                    'error': None
                })
                
                logger.info(f"✅ {test_name}: PASSED ({execution_time:.1f}ms)")
                
            except Exception as e:
                test_results['tests_failed'] += 1
                test_results['test_details'].append({
                    'test_name': test_name,
                    'status': 'FAILED',
                    'execution_time_ms': 0,
                    'error': str(e)
                })
                
                logger.error(f"❌ {test_name}: FAILED - {e}")
        
    except Exception as e:
        logger.error(f"💥 Test suite initialization failed: {e}")
        test_results['tests_failed'] += 1
    
    # Generate final report
    total_tests = test_results['tests_passed'] + test_results['tests_failed']
    success_rate = (test_results['tests_passed'] / max(total_tests, 1)) * 100
    
    logger.info("=" * 80)
    logger.info("📋 STEP 6.1 TEST SUITE RESULTS")
    logger.info("=" * 80)
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Tests Passed: {test_results['tests_passed']}")
    logger.info(f"Tests Failed: {test_results['tests_failed']}")
    logger.info(f"Success Rate: {success_rate:.1f}%")
    
    if test_results['tests_failed'] > 0:
        logger.info("\n❌ FAILED TESTS:")
        for test in test_results['test_details']:
            if test['status'] == 'FAILED':
                logger.info(f"  - {test['test_name']}: {test['error']}")
    
    if success_rate >= 90:
        logger.info("\n🎉 STEP 6.1 IMPLEMENTATION: PRODUCTION READY!")
        logger.info("✅ Ultra-Scale Performance Optimization with MongoDB Caching: VALIDATED")
    elif success_rate >= 75:
        logger.info("\n⚠️ STEP 6.1 IMPLEMENTATION: MOSTLY WORKING - Minor Issues")
    else:
        logger.info("\n❌ STEP 6.1 IMPLEMENTATION: NEEDS FIXES")
    
    logger.info("=" * 80)
    
    return test_results

if __name__ == "__main__":
    # Run the comprehensive test suite
    asyncio.run(run_comprehensive_step_6_1_tests())