"""
Advanced Legal Document Models for Ultra-Comprehensive Scraping System
Designed for 370M+ documents from 1,000+ sources with AI agent optimization
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid

class DocumentType(str, Enum):
    CASE_LAW = "case_law"
    STATUTE = "statute"
    REGULATION = "regulation"
    TREATY = "treaty"
    CONSTITUTIONAL = "constitutional"
    ADMINISTRATIVE = "administrative"
    JUDICIAL_OPINION = "judicial_opinion"
    COURT_ORDER = "court_order"
    LEGISLATIVE_BILL = "legislative_bill"
    EXECUTIVE_ORDER = "executive_order"
    AGENCY_GUIDANCE = "agency_guidance"
    LEGAL_BRIEF = "legal_brief"
    SCHOLARLY_ARTICLE = "scholarly_article"
    BAR_PUBLICATION = "bar_publication"
    LEGAL_NEWS = "legal_news"
    INTERNATIONAL_LAW = "international_law"

class JurisdictionLevel(str, Enum):
    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"
    INTERNATIONAL = "international"
    TRIBAL = "tribal"
    TERRITORIAL = "territorial"

class DocumentStatus(str, Enum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    PENDING = "pending"
    ARCHIVED = "archived"
    DRAFT = "draft"

class PrecedentialValue(str, Enum):
    BINDING = "binding"
    PERSUASIVE = "persuasive"
    INFORMATIONAL = "informational"
    HISTORICAL = "historical"

class ProcessingStatus(str, Enum):
    RAW = "raw"
    PROCESSED = "processed"
    ENHANCED = "enhanced"
    VALIDATED = "validated"
    INDEXED = "indexed"

# Core Legal Document Model
class LegalDocumentBase(BaseModel):
    title: str = Field(..., description="Document title or case name")
    content: str = Field(..., description="Full document text content")
    summary: Optional[str] = Field(None, description="AI-generated summary")
    document_type: DocumentType = Field(..., description="Type of legal document")
    jurisdiction: str = Field(..., description="Jurisdiction (e.g., 'United States', 'California', 'European Union')")
    jurisdiction_level: JurisdictionLevel = Field(..., description="Level of jurisdiction")
    
    # Court/Authority Information
    court: Optional[str] = Field(None, description="Court or issuing authority")
    judge: Optional[str] = Field(None, description="Judge or decision maker")
    
    # Date Information
    date_published: Optional[datetime] = Field(None, description="Publication/decision date")
    date_filed: Optional[datetime] = Field(None, description="Filing date")
    date_effective: Optional[datetime] = Field(None, description="Effective date")
    
    # Legal Citations
    citations: List[str] = Field(default_factory=list, description="Legal citations")
    parallel_citations: List[str] = Field(default_factory=list, description="Parallel citations")
    cited_cases: List[str] = Field(default_factory=list, description="Cases cited within document")
    
    # Legal Topics & Classification
    legal_topics: List[str] = Field(default_factory=list, description="Legal subject areas")
    practice_areas: List[str] = Field(default_factory=list, description="Practice area classifications")
    legal_concepts: List[str] = Field(default_factory=list, description="Specific legal concepts")
    
    # Parties & Entities
    parties: List[str] = Field(default_factory=list, description="Parties involved")
    attorneys: List[str] = Field(default_factory=list, description="Attorneys/law firms")
    
    # Document Relationships
    precedential_value: Optional[PrecedentialValue] = Field(None, description="Precedential authority")
    overruled_by: Optional[str] = Field(None, description="If overruled, reference to overruling case")
    related_documents: List[str] = Field(default_factory=list, description="Related document IDs")
    
    # Source & Processing Information
    source: str = Field(..., description="Source system (e.g., 'courtlistener', 'congress_gov')")
    source_url: str = Field(..., description="Original URL")
    source_id: Optional[str] = Field(None, description="Source-specific identifier")
    
    # Quality & Validation
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="AI confidence in extraction quality")
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Document completeness assessment")
    
class LegalDocument(LegalDocumentBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: DocumentStatus = Field(default=DocumentStatus.ACTIVE)
    processing_status: ProcessingStatus = Field(default=ProcessingStatus.RAW)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = Field(None)
    
    # Processing Metadata
    extraction_metadata: Dict[str, Any] = Field(default_factory=dict, description="AI extraction metadata")
    validation_results: Dict[str, Any] = Field(default_factory=dict, description="Quality validation results")
    enhancement_data: Dict[str, Any] = Field(default_factory=dict, description="AI enhancement data")
    
    # Full-text search optimization
    searchable_text: Optional[str] = Field(None, description="Processed text for search optimization")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")

class LegalDocumentCreate(LegalDocumentBase):
    pass

class LegalDocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    legal_topics: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    processing_status: Optional[ProcessingStatus] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Source Configuration Models
class SourceType(str, Enum):
    API = "api"
    WEB_SCRAPING = "web_scraping"
    RSS_FEED = "rss_feed"
    FILE_DOWNLOAD = "file_download"
    DATABASE_SYNC = "database_sync"

class SourceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    RATE_LIMITED = "rate_limited"

class LegalSource(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Source name")
    source_type: SourceType = Field(..., description="Type of data source")
    base_url: str = Field(..., description="Base URL or endpoint")
    jurisdiction: str = Field(..., description="Primary jurisdiction")
    document_types: List[DocumentType] = Field(..., description="Types of documents available")
    
    # Access Configuration
    api_key_required: bool = Field(default=False)
    rate_limit: Optional[int] = Field(None, description="Requests per hour")
    concurrent_limit: Optional[int] = Field(None, description="Concurrent connections")
    
    # Processing Configuration
    selectors: Dict[str, str] = Field(default_factory=dict, description="CSS selectors for web scraping")
    api_endpoints: Dict[str, str] = Field(default_factory=dict, description="API endpoint configurations")
    headers: Dict[str, str] = Field(default_factory=dict, description="Required HTTP headers")
    
    # Quality & Reliability
    reliability_score: float = Field(default=1.0, ge=0.0, le=1.0)
    last_successful_scrape: Optional[datetime] = Field(None)
    error_count: int = Field(default=0)
    status: SourceStatus = Field(default=SourceStatus.ACTIVE)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Scraping Job Models
class ScrapingJobType(str, Enum):
    FULL_SCRAPE = "full_scrape"
    INCREMENTAL = "incremental"
    TARGETED = "targeted"
    VALIDATION = "validation"

class ScrapingJobStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"

class LegalScrapingJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_name: str = Field(..., description="Human-readable job name")
    job_type: ScrapingJobType = Field(..., description="Type of scraping job")
    
    # Target Configuration
    target_sources: List[str] = Field(..., description="Source IDs to scrape")
    target_document_types: List[DocumentType] = Field(default_factory=list)
    target_jurisdictions: List[str] = Field(default_factory=list)
    target_count: Optional[int] = Field(None, description="Maximum documents to scrape")
    
    # Date Filters
    date_from: Optional[datetime] = Field(None, description="Start date for document filtering")
    date_to: Optional[datetime] = Field(None, description="End date for document filtering")
    
    # Processing Configuration
    priority: int = Field(default=5, ge=1, le=10, description="Job priority (1=highest, 10=lowest)")
    concurrent_workers: int = Field(default=10, ge=1, le=100)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    
    # Status & Progress
    status: ScrapingJobStatus = Field(default=ScrapingJobStatus.QUEUED)
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    documents_processed: int = Field(default=0)
    documents_successful: int = Field(default=0)
    documents_failed: int = Field(default=0)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(None)
    completed_at: Optional[datetime] = Field(None)
    estimated_completion: Optional[datetime] = Field(None)
    
    # Results & Errors
    error_log: List[Dict[str, Any]] = Field(default_factory=list)
    performance_metrics: Dict[str, Any] = Field(default_factory=dict)
    ai_insights: Dict[str, Any] = Field(default_factory=dict, description="AI-generated job insights")

# Search & Filter Models
class LegalDocumentFilter(BaseModel):
    document_types: Optional[List[DocumentType]] = None
    jurisdictions: Optional[List[str]] = None
    jurisdiction_levels: Optional[List[JurisdictionLevel]] = None
    courts: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    legal_topics: Optional[List[str]] = None
    practice_areas: Optional[List[str]] = None
    precedential_values: Optional[List[PrecedentialValue]] = None
    sources: Optional[List[str]] = None
    search_text: Optional[str] = None
    min_confidence_score: Optional[float] = None
    processing_status: Optional[List[ProcessingStatus]] = None

class LegalDocumentResponse(BaseModel):
    documents: List[LegalDocument]
    total_count: int
    page: int
    per_page: int
    total_pages: int
    filters_applied: LegalDocumentFilter
    search_metadata: Dict[str, Any] = Field(default_factory=dict)

# Analytics Models
class SourceAnalytics(BaseModel):
    source_id: str
    source_name: str
    total_documents: int
    documents_last_30_days: int
    success_rate: float
    average_processing_time: float
    document_type_distribution: Dict[DocumentType, int]
    jurisdiction_distribution: Dict[str, int]
    last_updated: datetime

class SystemMetrics(BaseModel):
    total_documents: int
    total_sources: int
    active_jobs: int
    documents_processed_today: int
    average_confidence_score: float
    source_distribution: List[SourceAnalytics]
    performance_metrics: Dict[str, Any]
    ai_insights: Dict[str, Any] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

# AI Enhancement Models
class AIProcessingTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str
    task_type: str  # "summarization", "classification", "citation_extraction", etc.
    priority: int = Field(default=5, ge=1, le=10)
    status: str = Field(default="queued")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None