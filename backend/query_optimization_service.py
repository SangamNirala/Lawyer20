"""
Query Optimization Service - Step 4.1 Implementation
Advanced Query Building and Optimization for 370M+ Document Queries
Intelligent query construction with geographic optimization
"""

import logging
import time
import hashlib
import statistics
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict
import re

from ultra_scale_api_models import (
    UltraSearchFilter, DateRange, GeographicFilter, ContentFilter, 
    QualityFilter, SearchResultAnalytics
)
from legal_models import LegalDocumentFilter, DocumentType, JurisdictionLevel, ProcessingStatus

logger = logging.getLogger(__name__)

class QueryComplexityAnalyzer:
    """Analyze and score query complexity for optimization"""
    
    def __init__(self):
        self.complexity_weights = {
            'text_search': 2.0,
            'multiple_jurisdictions': 1.5,
            'date_ranges': 1.2,
            'document_types': 0.8,
            'legal_topics': 1.0,
            'quality_filters': 1.3,
            'geographic_filters': 1.8,
            'content_filters': 2.2,
            'exclusions': 1.5
        }
    
    def analyze_complexity(self, search_filter: UltraSearchFilter) -> Dict[str, Any]:
        """Analyze query complexity and suggest optimizations"""
        complexity_score = 0.0
        complexity_factors = []
        
        # Text search complexity
        if search_filter.query_text:
            text_complexity = self._analyze_text_complexity(search_filter.query_text)
            complexity_score += text_complexity * self.complexity_weights['text_search']
            complexity_factors.append(f"Text search complexity: {text_complexity:.2f}")
        
        # Geographic complexity
        if search_filter.geographic:
            geo_complexity = self._analyze_geographic_complexity(search_filter.geographic)
            complexity_score += geo_complexity * self.complexity_weights['geographic_filters']
            complexity_factors.append(f"Geographic complexity: {geo_complexity:.2f}")
        
        # Date range complexity
        if search_filter.date_ranges:
            date_complexity = len(search_filter.date_ranges) * 0.5
            complexity_score += date_complexity * self.complexity_weights['date_ranges']
            complexity_factors.append(f"Date range complexity: {date_complexity:.2f}")
        
        # Document type complexity
        if search_filter.document_types:
            doc_type_complexity = min(len(search_filter.document_types) * 0.3, 2.0)
            complexity_score += doc_type_complexity * self.complexity_weights['document_types']
            complexity_factors.append(f"Document type complexity: {doc_type_complexity:.2f}")
        
        # Content filter complexity
        if search_filter.content:
            content_complexity = self._analyze_content_complexity(search_filter.content)
            complexity_score += content_complexity * self.complexity_weights['content_filters']
            complexity_factors.append(f"Content filter complexity: {content_complexity:.2f}")
        
        # Quality filter complexity
        if search_filter.quality:
            quality_complexity = self._analyze_quality_complexity(search_filter.quality)
            complexity_score += quality_complexity * self.complexity_weights['quality_filters']
            complexity_factors.append(f"Quality filter complexity: {quality_complexity:.2f}")
        
        # Exclusion complexity
        exclusion_count = 0
        if search_filter.exclude_document_types:
            exclusion_count += len(search_filter.exclude_document_types)
        if search_filter.exclude_sources:
            exclusion_count += len(search_filter.exclude_sources)
        if search_filter.geographic and search_filter.geographic.exclude_jurisdictions:
            exclusion_count += len(search_filter.geographic.exclude_jurisdictions)
        
        if exclusion_count > 0:
            exclusion_complexity = exclusion_count * 0.4
            complexity_score += exclusion_complexity * self.complexity_weights['exclusions']
            complexity_factors.append(f"Exclusion complexity: {exclusion_complexity:.2f}")
        
        # Normalize complexity score (0.0 to 10.0)
        normalized_score = min(complexity_score, 10.0)
        
        return {
            'complexity_score': normalized_score,
            'complexity_level': self._get_complexity_level(normalized_score),
            'complexity_factors': complexity_factors,
            'optimization_recommendations': self._get_optimization_recommendations(normalized_score, search_filter)
        }
    
    def _analyze_text_complexity(self, text: str) -> float:
        """Analyze text search complexity"""
        if not text:
            return 0.0
        
        complexity = 0.0
        
        # Length factor
        complexity += min(len(text) / 100.0, 2.0)
        
        # Boolean operators
        boolean_operators = len(re.findall(r'\b(AND|OR|NOT)\b', text, re.IGNORECASE))
        complexity += boolean_operators * 0.5
        
        # Quoted phrases
        quoted_phrases = len(re.findall(r'"[^"]*"', text))
        complexity += quoted_phrases * 0.3
        
        # Wildcards
        wildcards = len(re.findall(r'[*?]', text))
        complexity += wildcards * 0.2
        
        # Special characters
        special_chars = len(re.findall(r'[()[\]{}]', text))
        complexity += special_chars * 0.1
        
        return min(complexity, 5.0)
    
    def _analyze_geographic_complexity(self, geo_filter: GeographicFilter) -> float:
        """Analyze geographic filter complexity"""
        complexity = 0.0
        
        if geo_filter.jurisdictions:
            complexity += min(len(geo_filter.jurisdictions) * 0.2, 2.0)
        
        if geo_filter.jurisdiction_levels:
            complexity += len(geo_filter.jurisdiction_levels) * 0.1
        
        if geo_filter.regions:
            complexity += len(geo_filter.regions) * 0.3
        
        if geo_filter.countries:
            complexity += min(len(geo_filter.countries) * 0.2, 1.5)
        
        if geo_filter.exclude_jurisdictions:
            complexity += len(geo_filter.exclude_jurisdictions) * 0.3
        
        return min(complexity, 5.0)
    
    def _analyze_content_complexity(self, content_filter: ContentFilter) -> float:
        """Analyze content filter complexity"""
        complexity = 0.0
        
        if content_filter.legal_topics:
            complexity += min(len(content_filter.legal_topics) * 0.2, 2.0)
        
        if content_filter.practice_areas:
            complexity += min(len(content_filter.practice_areas) * 0.2, 1.5)
        
        if content_filter.legal_concepts:
            complexity += min(len(content_filter.legal_concepts) * 0.3, 2.0)
        
        if content_filter.keywords:
            complexity += min(len(content_filter.keywords) * 0.1, 1.0)
        
        if content_filter.exclude_keywords:
            complexity += len(content_filter.exclude_keywords) * 0.2
        
        return min(complexity, 5.0)
    
    def _analyze_quality_complexity(self, quality_filter: QualityFilter) -> float:
        """Analyze quality filter complexity"""
        complexity = 0.0
        
        if quality_filter.min_confidence_score and quality_filter.min_confidence_score > 0:
            complexity += 0.5
        
        if quality_filter.min_completeness_score and quality_filter.min_completeness_score > 0:
            complexity += 0.5
        
        if quality_filter.processing_status:
            complexity += len(quality_filter.processing_status) * 0.3
        
        if quality_filter.precedential_values:
            complexity += len(quality_filter.precedential_values) * 0.2
        
        if quality_filter.min_citation_count and quality_filter.min_citation_count > 0:
            complexity += 0.8
        
        return min(complexity, 3.0)
    
    def _get_complexity_level(self, score: float) -> str:
        """Get human-readable complexity level"""
        if score < 2.0:
            return "Low"
        elif score < 5.0:
            return "Medium"
        elif score < 8.0:
            return "High"
        else:
            return "Ultra-High"
    
    def _get_optimization_recommendations(self, score: float, search_filter: UltraSearchFilter) -> List[str]:
        """Get optimization recommendations based on complexity"""
        recommendations = []
        
        if score > 7.0:
            recommendations.append("Consider breaking this into multiple simpler queries")
            recommendations.append("Use result caching for repeated complex queries")
        
        if score > 5.0:
            recommendations.append("Enable query parallelization across shards")
            recommendations.append("Consider using asynchronous processing")
        
        if search_filter.query_text and len(search_filter.query_text) > 200:
            recommendations.append("Simplify text search query for better performance")
        
        if (search_filter.geographic and search_filter.geographic.jurisdictions and 
            len(search_filter.geographic.jurisdictions) > 10):
            recommendations.append("Limit jurisdiction search to most relevant ones")
        
        if search_filter.date_ranges and len(search_filter.date_ranges) > 3:
            recommendations.append("Consolidate date ranges where possible")
        
        return recommendations

class UltraScaleQueryBuilder:
    """Advanced query builder for ultra-scale document search"""
    
    def __init__(self):
        self.complexity_analyzer = QueryComplexityAnalyzer()
        self.query_cache = {}
        self.optimization_stats = defaultdict(int)
    
    def build_ultra_scale_query(
        self, 
        search_filter: UltraSearchFilter,
        optimize_for_performance: bool = True
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Build optimized MongoDB query from UltraSearchFilter
        Returns: (mongodb_query, query_metadata)
        """
        start_time = time.time()
        
        # Analyze query complexity
        complexity_analysis = self.complexity_analyzer.analyze_complexity(search_filter)
        
        # Build base query
        query = {}
        metadata = {
            'complexity_analysis': complexity_analysis,
            'optimizations_applied': [],
            'shard_routing_hints': [],
            'index_hints': [],
            'estimated_performance': 'unknown'
        }
        
        # 1. Text search optimization
        if search_filter.query_text:
            text_query, text_optimizations = self._build_text_search_query(
                search_filter.query_text, 
                search_filter.search_fields or ['title', 'content'],
                search_filter.search_operator
            )
            query.update(text_query)
            metadata['optimizations_applied'].extend(text_optimizations)
            metadata['index_hints'].append('fulltext_search_idx')
        
        # 2. Document type filtering
        if search_filter.document_types or search_filter.exclude_document_types:
            doc_type_query = self._build_document_type_query(
                search_filter.document_types,
                search_filter.exclude_document_types
            )
            query.update(doc_type_query)
            metadata['index_hints'].append('complex_query_idx')
        
        # 3. Geographic filtering with shard optimization
        if search_filter.geographic:
            geo_query, shard_hints = self._build_geographic_query(search_filter.geographic)
            query.update(geo_query)
            metadata['shard_routing_hints'].extend(shard_hints)
            metadata['index_hints'].append('jurisdiction_type_date_idx')
        
        # 4. Temporal filtering
        if search_filter.date_ranges:
            date_query, date_optimizations = self._build_date_range_query(search_filter.date_ranges)
            query.update(date_query)
            metadata['optimizations_applied'].extend(date_optimizations)
            metadata['index_hints'].append('dates_idx')
        
        # 5. Court filtering
        if search_filter.courts:
            court_query = self._build_court_query(search_filter.courts)
            query.update(court_query)
            metadata['index_hints'].append('court_jurisdiction_type_idx')
        
        # 6. Content-based filtering
        if search_filter.content:
            content_query, content_optimizations = self._build_content_query(search_filter.content)
            query.update(content_query)
            metadata['optimizations_applied'].extend(content_optimizations)
            metadata['index_hints'].append('topics_precedential_quality_idx')
        
        # 7. Quality filtering
        if search_filter.quality:
            quality_query = self._build_quality_query(search_filter.quality)
            query.update(quality_query)
            metadata['index_hints'].append('quality_metrics_idx')
        
        # 8. Source filtering
        if search_filter.sources or search_filter.exclude_sources:
            source_query = self._build_source_query(
                search_filter.sources,
                search_filter.exclude_sources,
                search_filter.source_reliability_min
            )
            query.update(source_query)
            metadata['index_hints'].append('source_status_quality_idx')
        
        # 9. Advanced optimizations
        if optimize_for_performance:
            query, additional_optimizations = self._apply_performance_optimizations(
                query, complexity_analysis['complexity_score']
            )
            metadata['optimizations_applied'].extend(additional_optimizations)
        
        # 10. Estimate query performance
        metadata['estimated_performance'] = self._estimate_query_performance(
            query, complexity_analysis['complexity_score']
        )
        
        # Record build time
        build_time = (time.time() - start_time) * 1000
        metadata['build_time_ms'] = build_time
        metadata['query_hash'] = self._generate_query_hash(search_filter)
        
        logger.info(f"Built ultra-scale query in {build_time:.2f}ms, "
                   f"complexity: {complexity_analysis['complexity_level']}")
        
        return query, metadata
    
    def _build_text_search_query(self, query_text: str, search_fields: List[str], 
                               operator: str) -> Tuple[Dict[str, Any], List[str]]:
        """Build optimized full-text search query"""
        optimizations = []
        
        # Use MongoDB text search for performance
        if len(search_fields) <= 3 and len(query_text) < 200:
            # Simple text search - use MongoDB's built-in text indexing
            query = {"$text": {"$search": query_text}}
            optimizations.append("mongodb_text_search")
        else:
            # Complex text search - use regex for more control
            if operator.upper() == "OR":
                # OR operation - search across multiple fields
                field_conditions = []
                for field in search_fields:
                    field_conditions.append({
                        field: {"$regex": query_text, "$options": "i"}
                    })
                query = {"$or": field_conditions}
                optimizations.append("multi_field_regex_or")
            else:
                # AND operation - require text in all specified fields
                field_conditions = {}
                for field in search_fields:
                    field_conditions[field] = {"$regex": query_text, "$options": "i"}
                query = {"$and": [field_conditions]}
                optimizations.append("multi_field_regex_and")
        
        return query, optimizations
    
    def _build_document_type_query(self, include_types: Optional[List[DocumentType]], 
                                 exclude_types: Optional[List[DocumentType]]) -> Dict[str, Any]:
        """Build document type filtering query"""
        query = {}
        
        if include_types and exclude_types:
            # Include some, exclude others
            query["document_type"] = {
                "$in": include_types,
                "$nin": exclude_types
            }
        elif include_types:
            # Only include specific types
            if len(include_types) == 1:
                query["document_type"] = include_types[0]
            else:
                query["document_type"] = {"$in": include_types}
        elif exclude_types:
            # Exclude specific types
            query["document_type"] = {"$nin": exclude_types}
        
        return query
    
    def _build_geographic_query(self, geo_filter: GeographicFilter) -> Tuple[Dict[str, Any], List[str]]:
        """Build geographic filtering query with shard routing hints"""
        query = {}
        shard_hints = []
        
        # Jurisdiction filtering
        if geo_filter.jurisdictions:
            if len(geo_filter.jurisdictions) == 1:
                query["jurisdiction"] = geo_filter.jurisdictions[0]
                shard_hints.append(f"primary_jurisdiction:{geo_filter.jurisdictions[0]}")
            else:
                query["jurisdiction"] = {"$in": geo_filter.jurisdictions}
                shard_hints.extend([f"jurisdiction:{j}" for j in geo_filter.jurisdictions])
        
        # Jurisdiction level filtering
        if geo_filter.jurisdiction_levels:
            if len(geo_filter.jurisdiction_levels) == 1:
                query["jurisdiction_level"] = geo_filter.jurisdiction_levels[0]
            else:
                query["jurisdiction_level"] = {"$in": geo_filter.jurisdiction_levels}
        
        # Regional filtering (using metadata or computed fields)
        if geo_filter.regions:
            # Assume we have a computed region field
            query["computed_region"] = {"$in": geo_filter.regions}
            shard_hints.extend([f"region:{r}" for r in geo_filter.regions])
        
        # Country filtering
        if geo_filter.countries:
            # Use regex to match country names within jurisdiction
            country_patterns = [f".*{country}.*" for country in geo_filter.countries]
            query["jurisdiction"] = {"$regex": "|".join(country_patterns), "$options": "i"}
        
        # Exclusion filtering
        if geo_filter.exclude_jurisdictions:
            exclude_condition = {"jurisdiction": {"$nin": geo_filter.exclude_jurisdictions}}
            if "$and" in query:
                query["$and"].append(exclude_condition)
            else:
                query = {"$and": [query, exclude_condition]} if query else exclude_condition
        
        return query, shard_hints
    
    def _build_date_range_query(self, date_ranges: List[DateRange]) -> Tuple[Dict[str, Any], List[str]]:
        """Build optimized date range query"""
        optimizations = []
        
        if len(date_ranges) == 1:
            # Single date range - optimize for simple query
            date_range = date_ranges[0]
            date_field = f"date_{date_range.date_type}"
            
            range_condition = {}
            if date_range.start_date:
                range_condition["$gte"] = date_range.start_date
            if date_range.end_date:
                range_condition["$lte"] = date_range.end_date
            
            query = {date_field: range_condition}
            optimizations.append("single_date_range")
            
        else:
            # Multiple date ranges - use $or for efficiency
            date_conditions = []
            
            for date_range in date_ranges:
                date_field = f"date_{date_range.date_type}"
                range_condition = {}
                
                if date_range.start_date:
                    range_condition["$gte"] = date_range.start_date
                if date_range.end_date:
                    range_condition["$lte"] = date_range.end_date
                
                if range_condition:
                    date_conditions.append({date_field: range_condition})
            
            query = {"$or": date_conditions} if date_conditions else {}
            optimizations.append("multi_date_range_or")
        
        return query, optimizations
    
    def _build_court_query(self, courts: List[str]) -> Dict[str, Any]:
        """Build court filtering query"""
        if len(courts) == 1:
            return {"court": courts[0]}
        else:
            return {"court": {"$in": courts}}
    
    def _build_content_query(self, content_filter: ContentFilter) -> Tuple[Dict[str, Any], List[str]]:
        """Build content-based filtering query"""
        query = {}
        optimizations = []
        
        # Legal topics
        if content_filter.legal_topics:
            query["legal_topics"] = {"$in": content_filter.legal_topics}
            optimizations.append("legal_topics_index")
        
        # Practice areas
        if content_filter.practice_areas:
            if "legal_topics" in query:
                # Combine with existing legal topics
                query["$and"] = [
                    {"legal_topics": query["legal_topics"]},
                    {"practice_areas": {"$in": content_filter.practice_areas}}
                ]
                del query["legal_topics"]
            else:
                query["practice_areas"] = {"$in": content_filter.practice_areas}
            optimizations.append("practice_areas_filter")
        
        # Legal concepts
        if content_filter.legal_concepts:
            query["legal_concepts"] = {"$in": content_filter.legal_concepts}
            optimizations.append("legal_concepts_filter")
        
        # Keywords in content
        if content_filter.keywords:
            keyword_conditions = []
            for keyword in content_filter.keywords:
                keyword_conditions.append({
                    "content": {"$regex": keyword, "$options": "i"}
                })
            
            if len(keyword_conditions) == 1:
                if "$and" in query:
                    query["$and"].append(keyword_conditions[0])
                else:
                    query.update(keyword_conditions[0])
            else:
                keyword_query = {"$and": keyword_conditions}
                if "$and" in query:
                    query["$and"].append(keyword_query)
                else:
                    query = {"$and": [query, keyword_query]} if query else keyword_query
            
            optimizations.append("keyword_content_search")
        
        # Exclude keywords
        if content_filter.exclude_keywords:
            for keyword in content_filter.exclude_keywords:
                exclude_condition = {
                    "content": {"$not": {"$regex": keyword, "$options": "i"}}
                }
                if "$and" in query:
                    query["$and"].append(exclude_condition)
                else:
                    query = {"$and": [query, exclude_condition]} if query else exclude_condition
            optimizations.append("keyword_exclusion")
        
        # Language filtering
        if content_filter.language:
            query["language"] = content_filter.language
            optimizations.append("language_filter")
        
        return query, optimizations
    
    def _build_quality_query(self, quality_filter: QualityFilter) -> Dict[str, Any]:
        """Build quality-based filtering query"""
        query = {}
        
        # Confidence score
        if quality_filter.min_confidence_score and quality_filter.min_confidence_score > 0:
            query["confidence_score"] = {"$gte": quality_filter.min_confidence_score}
        
        # Completeness score
        if quality_filter.min_completeness_score and quality_filter.min_completeness_score > 0:
            if "confidence_score" in query:
                query["$and"] = [
                    {"confidence_score": query["confidence_score"]},
                    {"completeness_score": {"$gte": quality_filter.min_completeness_score}}
                ]
                del query["confidence_score"]
            else:
                query["completeness_score"] = {"$gte": quality_filter.min_completeness_score}
        
        # Processing status
        if quality_filter.processing_status:
            status_condition = {"processing_status": {"$in": quality_filter.processing_status}}
            if "$and" in query:
                query["$and"].append(status_condition)
            elif query:
                query = {"$and": [query, status_condition]}
            else:
                query = status_condition
        
        # Precedential values
        if quality_filter.precedential_values:
            precedential_condition = {"precedential_value": {"$in": quality_filter.precedential_values}}
            if "$and" in query:
                query["$and"].append(precedential_condition)
            elif query:
                query = {"$and": [query, precedential_condition]}
            else:
                query = precedential_condition
        
        # Citation count
        if quality_filter.min_citation_count and quality_filter.min_citation_count > 0:
            citation_condition = {"citation_count": {"$gte": quality_filter.min_citation_count}}
            if "$and" in query:
                query["$and"].append(citation_condition)
            elif query:
                query = {"$and": [query, citation_condition]}
            else:
                query = citation_condition
        
        return query
    
    def _build_source_query(self, include_sources: Optional[List[str]], 
                          exclude_sources: Optional[List[str]], 
                          min_reliability: Optional[float]) -> Dict[str, Any]:
        """Build source-based filtering query"""
        query = {}
        
        # Include specific sources
        if include_sources:
            if len(include_sources) == 1:
                query["source"] = include_sources[0]
            else:
                query["source"] = {"$in": include_sources}
        
        # Exclude specific sources
        if exclude_sources:
            exclude_condition = {"source": {"$nin": exclude_sources}}
            if "$and" in query:
                query["$and"].append(exclude_condition)
            elif query:
                query = {"$and": [query, exclude_condition]}
            else:
                query = exclude_condition
        
        # Source reliability
        if min_reliability and min_reliability > 0:
            reliability_condition = {"source_reliability": {"$gte": min_reliability}}
            if "$and" in query:
                query["$and"].append(reliability_condition)
            elif query:
                query = {"$and": [query, reliability_condition]}
            else:
                query = reliability_condition
        
        return query
    
    def _apply_performance_optimizations(self, query: Dict[str, Any], 
                                       complexity_score: float) -> Tuple[Dict[str, Any], List[str]]:
        """Apply performance optimizations based on query complexity"""
        optimizations = []
        
        # For high complexity queries, add query hints
        if complexity_score > 6.0:
            # Add query timeout to prevent runaway queries
            query["$maxTimeMS"] = 30000  # 30 second timeout
            optimizations.append("query_timeout_30s")
            
            # Suggest using allowPartialResults for very large result sets
            optimizations.append("suggest_partial_results")
        
        # Optimize $and conditions
        if "$and" in query and len(query["$and"]) > 1:
            # Reorder $and conditions by selectivity (most selective first)
            query["$and"] = self._reorder_and_conditions(query["$and"])
            optimizations.append("reordered_and_conditions")
        
        # Add query plan caching hints for repeated queries
        if complexity_score > 3.0:
            optimizations.append("enable_query_plan_cache")
        
        return query, optimizations
    
    def _reorder_and_conditions(self, and_conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reorder AND conditions by estimated selectivity"""
        # Simple heuristic: put exact matches first, then ranges, then regex last
        def selectivity_score(condition):
            if isinstance(condition, dict):
                for key, value in condition.items():
                    if isinstance(value, str):
                        return 1  # Exact string match - highest selectivity
                    elif isinstance(value, dict):
                        if "$in" in value:
                            return 2  # IN clause - medium selectivity
                        elif "$gte" in value or "$lte" in value:
                            return 3  # Range query - lower selectivity
                        elif "$regex" in value:
                            return 4  # Regex - lowest selectivity
            return 5  # Unknown - lowest priority
        
        return sorted(and_conditions, key=selectivity_score)
    
    def _estimate_query_performance(self, query: Dict[str, Any], complexity_score: float) -> str:
        """Estimate query performance based on structure and complexity"""
        if complexity_score < 2.0:
            return "Fast (<100ms)"
        elif complexity_score < 4.0:
            return "Medium (100-500ms)"
        elif complexity_score < 7.0:
            return "Slow (500ms-2s)"
        else:
            return "Very Slow (>2s)"
    
    def _generate_query_hash(self, search_filter: UltraSearchFilter) -> str:
        """Generate hash for query caching"""
        query_str = str(search_filter.dict(exclude_none=True))
        return hashlib.md5(query_str.encode()).hexdigest()

def convert_ultra_filter_to_legacy(ultra_filter: UltraSearchFilter) -> LegalDocumentFilter:
    """Convert UltraSearchFilter to legacy LegalDocumentFilter for compatibility"""
    
    # Extract basic filters
    jurisdictions = None
    if ultra_filter.geographic and ultra_filter.geographic.jurisdictions:
        jurisdictions = ultra_filter.geographic.jurisdictions
    
    jurisdiction_levels = None
    if ultra_filter.geographic and ultra_filter.geographic.jurisdiction_levels:
        jurisdiction_levels = ultra_filter.geographic.jurisdiction_levels
    
    legal_topics = None
    if ultra_filter.content and ultra_filter.content.legal_topics:
        legal_topics = ultra_filter.content.legal_topics
    
    practice_areas = None
    if ultra_filter.content and ultra_filter.content.practice_areas:
        practice_areas = ultra_filter.content.practice_areas
    
    precedential_values = None
    if ultra_filter.quality and ultra_filter.quality.precedential_values:
        precedential_values = ultra_filter.quality.precedential_values
    
    processing_status = None
    if ultra_filter.quality and ultra_filter.quality.processing_status:
        processing_status = ultra_filter.quality.processing_status
    
    min_confidence_score = None
    if ultra_filter.quality and ultra_filter.quality.min_confidence_score:
        min_confidence_score = ultra_filter.quality.min_confidence_score
    
    # Handle date ranges (use first one if multiple)
    date_from = None
    date_to = None
    if ultra_filter.date_ranges and len(ultra_filter.date_ranges) > 0:
        first_range = ultra_filter.date_ranges[0]
        date_from = first_range.start_date
        date_to = first_range.end_date
    
    return LegalDocumentFilter(
        document_types=ultra_filter.document_types,
        jurisdictions=jurisdictions,
        jurisdiction_levels=jurisdiction_levels,
        courts=ultra_filter.courts,
        date_from=date_from,
        date_to=date_to,
        legal_topics=legal_topics,
        practice_areas=practice_areas,
        precedential_values=precedential_values,
        sources=ultra_filter.sources,
        search_text=ultra_filter.query_text,
        min_confidence_score=min_confidence_score,
        processing_status=processing_status
    )