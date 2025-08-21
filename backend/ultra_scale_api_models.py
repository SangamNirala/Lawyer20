"""
Ultra-Scale API Models - Step 4.1 Implementation
Advanced Response Models for 370M+ Document API System
Designed for ultra-comprehensive legal document search and monitoring
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from enum import Enum
import uuid

from legal_models import (
    LegalDocument, DocumentType, JurisdictionLevel, 
    ProcessingStatus, PrecedentialValue
)

# ================================================================================================
# ADVANCED QUERY AND FILTER MODELS
# ================================================================================================

class DateRange(BaseModel):
    """Advanced date range model for temporal queries"""
    start_date: Optional[datetime] = Field(None, description="Start date for range query")
    end_date: Optional[datetime] = Field(None, description="End date for range query")
    date_type: str = Field("published", description="Type of date to filter on (published, filed, effective)")
    
    @validator('end_date')
    def end_date_must_be_after_start(cls, v, values):
        if v is not None and 'start_date' in values and values['start_date'] is not None:
            if v <= values['start_date']:
                raise ValueError('end_date must be after start_date')
        return v

class GeographicFilter(BaseModel):
    """Advanced geographic filtering with regional optimization"""
    jurisdictions: Optional[List[str]] = Field(None, description="Specific jurisdictions to search")
    jurisdiction_levels: Optional[List[JurisdictionLevel]] = Field(None, description="Jurisdiction levels to include")
    regions: Optional[List[str]] = Field(None, description="Geographic regions (e.g., 'North America', 'Europe')")
    countries: Optional[List[str]] = Field(None, description="Specific countries")
    exclude_jurisdictions: Optional[List[str]] = Field(None, description="Jurisdictions to exclude")

class ContentFilter(BaseModel):
    """Advanced content-based filtering"""
    legal_topics: Optional[List[str]] = Field(None, description="Legal topic categories")
    practice_areas: Optional[List[str]] = Field(None, description="Legal practice areas")
    legal_concepts: Optional[List[str]] = Field(None, description="Specific legal concepts")
    keywords: Optional[List[str]] = Field(None, description="Keywords to search for")
    exclude_keywords: Optional[List[str]] = Field(None, description="Keywords to exclude")
    language: Optional[str] = Field(None, description="Document language")

class QualityFilter(BaseModel):
    """Advanced quality and reliability filtering"""
    min_confidence_score: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="Minimum confidence score")
    min_completeness_score: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="Minimum completeness score")
    processing_status: Optional[List[ProcessingStatus]] = Field(None, description="Processing status filter")
    precedential_values: Optional[List[PrecedentialValue]] = Field(None, description="Precedential authority filter")
    min_citation_count: Optional[int] = Field(None, ge=0, description="Minimum number of citations")

class UltraSearchFilter(BaseModel):
    """Comprehensive ultra-scale search filter combining all criteria"""
    # Text Search
    query_text: Optional[str] = Field(None, description="Full-text search query")
    search_fields: Optional[List[str]] = Field(
        ["title", "content"], 
        description="Fields to search in"
    )
    search_operator: str = Field("AND", description="Search operator (AND, OR)")
    
    # Document Classification
    document_types: Optional[List[DocumentType]] = Field(None, description="Document types to include")
    exclude_document_types: Optional[List[DocumentType]] = Field(None, description="Document types to exclude")
    
    # Geographic & Jurisdictional
    geographic: Optional[GeographicFilter] = Field(None, description="Geographic filtering")
    courts: Optional[List[str]] = Field(None, description="Specific courts")
    
    # Temporal
    date_ranges: Optional[List[DateRange]] = Field(None, description="Date range filters")
    
    # Content-Based
    content: Optional[ContentFilter] = Field(None, description="Content-based filtering")
    
    # Quality & Reliability
    quality: Optional[QualityFilter] = Field(None, description="Quality filtering")
    
    # Source-Based
    sources: Optional[List[str]] = Field(None, description="Specific sources to search")
    exclude_sources: Optional[List[str]] = Field(None, description="Sources to exclude")
    source_reliability_min: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum source reliability")
    
    # Advanced Options
    similarity_threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Similarity threshold for duplicates")
    max_results_per_shard: Optional[int] = Field(1000, description="Maximum results per shard")
    boost_recent: Optional[bool] = Field(False, description="Boost more recent documents")

# ================================================================================================
# ULTRA-SCALE RESPONSE MODELS
# ================================================================================================

class DocumentSummary(BaseModel):
    """Optimized document summary for large result sets"""
    id: str = Field(..., description="Document identifier")
    title: str = Field(..., description="Document title")
    document_type: DocumentType = Field(..., description="Document type")
    jurisdiction: str = Field(..., description="Jurisdiction")
    court: Optional[str] = Field(None, description="Court or authority")
    date_published: Optional[datetime] = Field(None, description="Publication date")
    confidence_score: float = Field(..., description="AI confidence score")
    source: str = Field(..., description="Source identifier")
    snippet: Optional[str] = Field(None, description="Text snippet with highlights")
    relevance_score: Optional[float] = Field(None, description="Search relevance score")
    shard_source: Optional[str] = Field(None, description="Originating database shard")

class SearchResultAnalytics(BaseModel):
    """Advanced analytics for search results"""
    query_complexity_score: float = Field(..., description="Complexity of the executed query")
    shards_queried: int = Field(..., description="Number of database shards queried")
    total_documents_scanned: int = Field(..., description="Total documents examined")
    search_time_breakdown: Dict[str, float] = Field(..., description="Time spent in different search phases")
    optimization_applied: List[str] = Field(..., description="Query optimizations that were applied")
    cache_hit_rate: float = Field(..., description="Percentage of results served from cache")

class JurisdictionDistribution(BaseModel):
    """Distribution of results across jurisdictions"""
    jurisdiction: str = Field(..., description="Jurisdiction name")
    document_count: int = Field(..., description="Number of documents")
    percentage: float = Field(..., description="Percentage of total results")
    average_quality_score: float = Field(..., description="Average quality score for this jurisdiction")

class DocumentTypeDistribution(BaseModel):
    """Distribution of results by document type"""
    document_type: DocumentType = Field(..., description="Document type")
    count: int = Field(..., description="Number of documents")
    percentage: float = Field(..., description="Percentage of total results")

class TemporalDistribution(BaseModel):
    """Temporal distribution of search results"""
    year: int = Field(..., description="Year")
    month: Optional[int] = Field(None, description="Month (if available)")
    document_count: int = Field(..., description="Number of documents")
    percentage: float = Field(..., description="Percentage of total results")

class QualityDistribution(BaseModel):
    """Quality score distribution of results"""
    quality_range: str = Field(..., description="Quality score range (e.g., '0.8-0.9')")
    document_count: int = Field(..., description="Number of documents in range")
    percentage: float = Field(..., description="Percentage of total results")
    average_confidence: float = Field(..., description="Average confidence in this range")

class UltraSearchResponse(BaseModel):
    """Ultra-comprehensive search response for 370M+ document queries"""
    # Core Results
    documents: List[DocumentSummary] = Field(..., description="Search result documents")
    total_count: int = Field(..., description="Total number of matching documents")
    returned_count: int = Field(..., description="Number of documents in this response")
    
    # Pagination
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Results per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next_page: bool = Field(..., description="Whether there are more pages")
    
    # Search Metadata
    search_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique search identifier")
    execution_time_ms: float = Field(..., description="Total search execution time")
    search_analytics: SearchResultAnalytics = Field(..., description="Detailed search analytics")
    
    # Geographic Coverage
    jurisdictions_covered: List[str] = Field(..., description="Jurisdictions found in results")
    jurisdiction_distribution: List[JurisdictionDistribution] = Field(..., description="Distribution across jurisdictions")
    
    # Source Coverage
    sources_searched: List[str] = Field(..., description="Sources included in search")
    sources_with_results: List[str] = Field(..., description="Sources that returned results")
    
    # Content Analysis
    document_type_distribution: List[DocumentTypeDistribution] = Field(..., description="Distribution by document type")
    temporal_distribution: List[TemporalDistribution] = Field(..., description="Temporal distribution of results")
    quality_distribution: List[QualityDistribution] = Field(..., description="Quality score distribution")
    
    # Advanced Insights
    legal_topics_found: List[Dict[str, Any]] = Field(..., description="Legal topics discovered in results")
    citation_network_metrics: Dict[str, Any] = Field(..., description="Citation network analysis")
    
    # Query Information
    original_query: UltraSearchFilter = Field(..., description="Original search parameters")
    suggested_refinements: List[Dict[str, Any]] = Field(..., description="AI-suggested query refinements")
    
    # System Performance
    system_load_impact: Dict[str, Any] = Field(..., description="Impact on system resources")

# ================================================================================================
# SOURCE HEALTH AND MONITORING MODELS
# ================================================================================================

class SourceStatus(str, Enum):
    """Enhanced source status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive" 
    ERROR = "error"
    MAINTENANCE = "maintenance"
    RATE_LIMITED = "rate_limited"
    DEGRADED = "degraded"
    RECOVERING = "recovering"

class SourceHealthMetrics(BaseModel):
    """Comprehensive source health metrics"""
    source_id: str = Field(..., description="Source identifier")
    name: str = Field(..., description="Source display name")
    status: SourceStatus = Field(..., description="Current source status")
    
    # Performance Metrics
    documents_scraped: int = Field(..., description="Total documents scraped")
    documents_processed: int = Field(..., description="Total documents processed")
    success_rate: float = Field(..., description="Overall success rate (0.0 to 1.0)")
    error_rate: float = Field(..., description="Current error rate")
    
    # Timing Information
    last_successful_scrape: Optional[datetime] = Field(None, description="Last successful scraping operation")
    last_attempt: Optional[datetime] = Field(None, description="Last scraping attempt")
    average_response_time_ms: float = Field(..., description="Average response time")
    
    # Capacity and Estimates
    estimated_total_documents: Optional[int] = Field(None, description="Estimated total documents available")
    estimated_remaining: Optional[int] = Field(None, description="Estimated documents remaining")
    completion_percentage: Optional[float] = Field(None, description="Percentage of source completed")
    estimated_completion_date: Optional[datetime] = Field(None, description="Estimated completion date")
    
    # Quality Metrics
    average_quality_score: float = Field(..., description="Average quality score of documents")
    duplicate_rate: float = Field(..., description="Rate of duplicate documents detected")
    processing_efficiency: float = Field(..., description="Processing efficiency score")
    
    # Resource Usage
    bandwidth_usage_mb: float = Field(..., description="Total bandwidth used (MB)")
    requests_per_hour: float = Field(..., description="Current request rate")
    rate_limit_status: Dict[str, Any] = Field(..., description="Rate limiting status")
    
    # Geographic/Regional Info
    jurisdiction: str = Field(..., description="Primary jurisdiction")
    region: str = Field(..., description="Geographic region")
    priority_tier: int = Field(..., description="Priority tier (1=highest)")

class RegionalHealthSummary(BaseModel):
    """Health summary by geographic region"""
    region: str = Field(..., description="Geographic region")
    total_sources: int = Field(..., description="Total sources in region")
    active_sources: int = Field(..., description="Currently active sources")
    total_documents: int = Field(..., description="Total documents from region")
    average_success_rate: float = Field(..., description="Average success rate for region")
    last_update: datetime = Field(..., description="Last update timestamp")

class SystemCapacityMetrics(BaseModel):
    """System-wide capacity and performance metrics"""
    total_processing_capacity: int = Field(..., description="Total processing capacity (docs/hour)")
    current_utilization: float = Field(..., description="Current capacity utilization (0.0 to 1.0)")
    peak_utilization_24h: float = Field(..., description="Peak utilization in last 24 hours")
    estimated_time_to_370m: Optional[int] = Field(None, description="Estimated hours to reach 370M documents")
    bottleneck_analysis: List[Dict[str, Any]] = Field(..., description="Identified system bottlenecks")

class SourceHealthDashboard(BaseModel):
    """Comprehensive source health dashboard for 1,600+ sources"""
    # Summary Statistics
    total_sources: int = Field(..., description="Total number of configured sources")
    active_sources: int = Field(..., description="Currently active sources")
    inactive_sources: int = Field(..., description="Inactive sources")
    error_sources: int = Field(..., description="Sources in error state")
    
    # Global Metrics
    total_documents: int = Field(..., description="Total documents scraped across all sources")
    documents_last_24h: int = Field(..., description="Documents scraped in last 24 hours")
    overall_success_rate: float = Field(..., description="Global success rate")
    
    # Performance Indicators
    average_response_time_ms: float = Field(..., description="Average response time across all sources")
    peak_throughput_docs_per_hour: int = Field(..., description="Peak throughput achieved")
    current_throughput_docs_per_hour: int = Field(..., description="Current throughput")
    
    # Detailed Source Metrics
    source_metrics: List[SourceHealthMetrics] = Field(..., description="Individual source metrics")
    
    # Regional Analysis
    regional_summaries: List[RegionalHealthSummary] = Field(..., description="Health by geographic region")
    
    # System Capacity
    capacity_metrics: SystemCapacityMetrics = Field(..., description="System capacity analysis")
    
    # Alerts and Issues
    critical_issues: List[Dict[str, Any]] = Field(..., description="Critical issues requiring attention")
    warnings: List[Dict[str, Any]] = Field(..., description="Warning-level issues")
    
    # Trends and Predictions
    performance_trends: Dict[str, Any] = Field(..., description="Performance trend analysis")
    capacity_predictions: Dict[str, Any] = Field(..., description="Capacity and growth predictions")
    
    # Last Updated
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Dashboard last update time")
    update_frequency_minutes: int = Field(5, description="Dashboard update frequency")

# ================================================================================================
# SYSTEM ANALYTICS AND MONITORING MODELS
# ================================================================================================

class SystemPerformanceMetrics(BaseModel):
    """System-wide performance metrics"""
    cpu_utilization: float = Field(..., description="CPU utilization percentage")
    memory_utilization: float = Field(..., description="Memory utilization percentage") 
    disk_utilization: float = Field(..., description="Disk utilization percentage")
    network_throughput_mbps: float = Field(..., description="Network throughput in Mbps")
    database_connections: int = Field(..., description="Active database connections")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    average_query_time_ms: float = Field(..., description="Average database query time")

class ScalingMetrics(BaseModel):
    """Auto-scaling and capacity metrics"""
    current_instance_count: int = Field(..., description="Current number of instances")
    target_instance_count: int = Field(..., description="Target number of instances")
    scaling_events_24h: int = Field(..., description="Scaling events in last 24 hours")
    load_balancer_status: str = Field(..., description="Load balancer status")
    geographic_distribution: Dict[str, int] = Field(..., description="Instance distribution by region")

class APIAnalytics(BaseModel):
    """API usage and performance analytics"""
    total_requests_24h: int = Field(..., description="Total API requests in 24 hours")
    successful_requests: int = Field(..., description="Successful requests")
    failed_requests: int = Field(..., description="Failed requests")
    average_response_time_ms: float = Field(..., description="Average API response time")
    p95_response_time_ms: float = Field(..., description="95th percentile response time")
    rate_limited_requests: int = Field(..., description="Rate limited requests")
    
    # Endpoint-specific metrics
    endpoint_metrics: Dict[str, Dict[str, Any]] = Field(..., description="Per-endpoint performance metrics")
    
    # Geographic distribution of requests
    request_by_region: Dict[str, int] = Field(..., description="Requests by geographic region")

class UltraScaleSystemStatus(BaseModel):
    """Complete system status for ultra-scale operations"""
    # Overall Status
    system_status: str = Field(..., description="Overall system status")
    operational_level: float = Field(..., description="Operational level (0.0 to 1.0)")
    
    # Core Metrics
    performance_metrics: SystemPerformanceMetrics = Field(..., description="System performance metrics")
    scaling_metrics: ScalingMetrics = Field(..., description="Scaling and capacity metrics")
    api_analytics: APIAnalytics = Field(..., description="API usage analytics")
    
    # Database Status (from Step 3.1)
    database_status: Dict[str, Any] = Field(..., description="Ultra-scale database status")
    shard_health: Dict[str, Any] = Field(..., description="Individual shard health status")
    
    # Processing Pipeline Status (from Steps 2.1-2.2)
    processing_pipeline_status: Dict[str, Any] = Field(..., description="Document processing pipeline status")
    
    # Source Integration Status
    source_integration_status: SourceHealthDashboard = Field(..., description="Source health dashboard")
    
    # Alerts and Notifications
    active_alerts: List[Dict[str, Any]] = Field(..., description="Active system alerts")
    recent_incidents: List[Dict[str, Any]] = Field(..., description="Recent incidents")
    
    # Capacity Planning
    capacity_forecast: Dict[str, Any] = Field(..., description="Capacity planning and forecasts")
    resource_recommendations: List[Dict[str, Any]] = Field(..., description="Resource optimization recommendations")
    
    # Timestamp
    status_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status generation timestamp")

# ================================================================================================
# PAGINATION AND NAVIGATION MODELS
# ================================================================================================

class PaginationInfo(BaseModel):
    """Advanced pagination with performance optimization"""
    current_page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Results per page")
    total_pages: int = Field(..., description="Total number of pages") 
    total_results: int = Field(..., description="Total number of results")
    has_previous: bool = Field(..., description="Whether there is a previous page")
    has_next: bool = Field(..., description="Whether there is a next page")
    
    # Performance optimizations
    cursor_token: Optional[str] = Field(None, description="Cursor token for efficient pagination")
    estimated_total: bool = Field(False, description="Whether total count is estimated")
    next_page_url: Optional[str] = Field(None, description="Direct URL for next page")
    previous_page_url: Optional[str] = Field(None, description="Direct URL for previous page")

class SortOptions(BaseModel):
    """Advanced sorting options for large result sets"""
    field: str = Field(..., description="Field to sort by")
    direction: str = Field("desc", description="Sort direction (asc/desc)")
    secondary_sort: Optional[str] = Field(None, description="Secondary sort field")
    relevance_boost: bool = Field(False, description="Apply relevance boosting")

# ================================================================================================
# EXPORT AND BULK OPERATIONS MODELS  
# ================================================================================================

class ExportFormat(str, Enum):
    """Available export formats"""
    JSON = "json"
    XML = "xml" 
    CSV = "csv"
    PDF = "pdf"
    EXCEL = "xlsx"

class BulkExportRequest(BaseModel):
    """Request model for bulk document export"""
    search_filter: UltraSearchFilter = Field(..., description="Search criteria for export")
    export_format: ExportFormat = Field(..., description="Export format")
    include_full_content: bool = Field(False, description="Include full document content")
    max_documents: int = Field(10000, le=100000, description="Maximum documents to export")
    email_notification: Optional[str] = Field(None, description="Email for completion notification")
    compression: bool = Field(True, description="Compress exported file")

class BulkExportStatus(BaseModel):
    """Status of bulk export operation"""
    export_id: str = Field(..., description="Export operation identifier")
    status: str = Field(..., description="Export status")
    progress_percentage: float = Field(..., description="Completion percentage")
    documents_processed: int = Field(..., description="Documents processed so far")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    download_url: Optional[str] = Field(None, description="Download URL when ready")
    file_size_mb: Optional[float] = Field(None, description="File size in MB")
    error_message: Optional[str] = Field(None, description="Error message if failed")