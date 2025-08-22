from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import asyncio

from models import (
    Question, QuestionCreate, QuestionUpdate, QuestionFilter, QuestionResponse,
    Category, CategoryCreate, ScrapingJob, ScrapingJobCreate, ScrapingJobUpdate,
    DashboardStats, SystemHealth, ScrapingStatus, QuestionStatus, DifficultyLevel
)
from database_service import DatabaseService
from scraper_engine import IndiaBixScraper
from scraper_config import INDIABIX_CONFIG

# Import ultra-scale components (Step 4.1)
try:
    from ultra_scale_api_endpoints import ultra_api_router
    ULTRA_SCALE_API_AVAILABLE = True
    logging.info("✅ Ultra-scale API endpoints loaded successfully")
except ImportError as e:
    ULTRA_SCALE_API_AVAILABLE = False
    logging.warning(f"⚠️ Ultra-scale API endpoints not available: {e}")

# Import legal scraping components (Steps 2.1-3.1)
try:
    from ultra_scale_scraping_engine import UltraScaleScrapingEngine
    from enhanced_legal_sources_config import ULTRA_COMPREHENSIVE_SOURCES
    LEGAL_SCRAPING_AVAILABLE = True
    logging.info("✅ Legal scraping components loaded successfully")
except ImportError as e:
    LEGAL_SCRAPING_AVAILABLE = False
    logging.warning(f"⚠️ Legal scraping components not available: {e}")

# Import Step 6.1 Performance Optimization components
try:
    from ultra_scale_performance_api import performance_api_router
    PERFORMANCE_OPTIMIZATION_AVAILABLE = True
    logging.info("✅ Performance optimization API loaded successfully")
except ImportError as e:
    PERFORMANCE_OPTIMIZATION_AVAILABLE = False
    logging.warning(f"⚠️ Performance optimization API not available: {e}")

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize database service
db_service = DatabaseService(db)

# Create the main app without a prefix
app = FastAPI(
    title="Aptitude Question Bank API",
    description="Comprehensive API for managing aptitude questions with web scraping capabilities",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class ScrapingJobRequest(BaseModel):
    job_name: str = Field(..., description="Name for the scraping job")
    categories: List[str] = Field(default_factory=list, description="Categories to scrape (empty for all)")
    target_count: int = Field(default=1000, description="Target number of questions")
    
class ScrapingStartResponse(BaseModel):
    job_id: str
    message: str
    estimated_duration: str

# Storage for active scraping jobs
active_scraping_jobs = {}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await db_service.initialize_database()
        logging.info("Database service initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database service: {e}")

# Basic Routes
@api_router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Aptitude Question Bank API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@api_router.get("/api-info")
async def get_api_info():
    """Get comprehensive API information and available features"""
    return {
        "api_name": "Aptitude Question Bank API",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "features": {
            "aptitude_questions": True,
            "web_scraping": True,
            "ultra_scale_api": ULTRA_SCALE_API_AVAILABLE,
            "legal_document_processing": LEGAL_SCRAPING_AVAILABLE,
            "performance_optimization": PERFORMANCE_OPTIMIZATION_AVAILABLE
        },
        "endpoints": {
            "core_endpoints": {
                "questions": "/api/questions",
                "categories": "/api/categories", 
                "scraping": "/api/scraping",
                "dashboard": "/api/dashboard"
            },
            "ultra_scale_endpoints": {
                "ultra_search": "/api/ultra-search" if ULTRA_SCALE_API_AVAILABLE else "not_available",
                "source_health": "/api/source-health" if ULTRA_SCALE_API_AVAILABLE else "not_available",
                "system_status": "/api/system-status" if ULTRA_SCALE_API_AVAILABLE else "not_available",
                "bulk_export": "/api/bulk-export" if ULTRA_SCALE_API_AVAILABLE else "not_available",
                "analytics": "/api/analytics" if ULTRA_SCALE_API_AVAILABLE else "not_available"
            },
            "performance_optimization_endpoints": {
                "optimize_query": "/api/performance/optimize-query" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "not_available",
                "performance_dashboard": "/api/performance/dashboard" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "not_available", 
                "cache_metrics": "/api/performance/cache-metrics" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "not_available",
                "system_status": "/api/performance/system-status" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "not_available",
                "cache_management": "/api/performance/cache-management" if PERFORMANCE_OPTIMIZATION_AVAILABLE else "not_available"
            }
        },
        "database": {
            "connection": "active",
            "name": os.environ.get('DB_NAME', 'aptitude_db'),
            "ultra_scale_shards": 8 if ULTRA_SCALE_API_AVAILABLE else 0
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        }
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    """Create a status check entry"""
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    """Get all status checks"""
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Dashboard Routes
@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    try:
        stats = await db_service.get_dashboard_stats()
        return stats
    except Exception as e:
        logging.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard stats")

@api_router.get("/dashboard/health", response_model=SystemHealth)
async def get_system_health():
    """Get system health status"""
    try:
        # Basic health checks
        health = SystemHealth()
        
        # Check database connectivity
        try:
            await db.command("ping")
            health.database_status = "healthy"
        except Exception:
            health.database_status = "unhealthy"
            health.errors.append("Database connection failed")
        
        # Check if Chrome driver is available
        try:
            import subprocess
            result = subprocess.run(['chromedriver', '--version'], capture_output=True, timeout=5)
            if result.returncode == 0:
                health.chrome_driver_status = "healthy"
            else:
                health.chrome_driver_status = "unhealthy"
                health.warnings.append("ChromeDriver version check failed")
        except Exception:
            health.chrome_driver_status = "unhealthy"
            health.errors.append("ChromeDriver not accessible")
        
        # Check scraping service status
        if active_scraping_jobs:
            health.scraping_service_status = "active"
            health.active_connections = len(active_scraping_jobs)
        else:
            health.scraping_service_status = "idle"
        
        return health
        
    except Exception as e:
        logging.error(f"Error getting system health: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve system health")

# Question Management Routes
@api_router.get("/questions", response_model=QuestionResponse)
async def get_questions(
    page: int = 1,
    per_page: int = 20,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    difficulty: Optional[DifficultyLevel] = None,
    status: Optional[QuestionStatus] = None,
    min_quality_score: Optional[int] = None,
    search: Optional[str] = None,
    source: Optional[str] = None
):
    """Get questions with filtering and pagination"""
    try:
        filter_params = QuestionFilter(
            category=category,
            subcategory=subcategory,
            difficulty=difficulty,
            status=status,
            min_quality_score=min_quality_score,
            search_text=search,
            source=source
        )
        
        response = await db_service.get_questions(filter_params, page, per_page)
        return response
        
    except Exception as e:
        logging.error(f"Error getting questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve questions")

@api_router.post("/questions", response_model=Question)
async def create_question(question_data: QuestionCreate):
    """Create a new question"""
    try:
        question = await db_service.create_question(question_data)
        return question
    except Exception as e:
        logging.error(f"Error creating question: {e}")
        raise HTTPException(status_code=500, detail="Failed to create question")

@api_router.put("/questions/{question_id}", response_model=Question)
async def update_question(question_id: str, question_data: QuestionUpdate):
    """Update an existing question"""
    try:
        question = await db_service.update_question(question_id, question_data)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating question {question_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update question")

@api_router.delete("/questions/{question_id}")
async def delete_question(question_id: str):
    """Delete a question (soft delete)"""
    try:
        success = await db_service.delete_question(question_id)
        if not success:
            raise HTTPException(status_code=404, detail="Question not found")
        return {"message": "Question deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting question {question_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete question")

# Category Management Routes
@api_router.get("/categories", response_model=List[Category])
async def get_categories():
    """Get all categories"""
    try:
        categories = await db_service.get_categories()
        return categories
    except Exception as e:
        logging.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")

# Legal Document Extraction Results
@api_router.get("/extraction/results")
async def get_extraction_results():
    """Get comprehensive legal document extraction results and statistics"""
    try:
        import pymongo
        from datetime import datetime
        import json
        
        # Connect to extraction database
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
        client = pymongo.MongoClient(mongo_url)
        db = client['legal_extraction_demo']
        
        # Get all collections (sources)
        collections = db.list_collection_names()
        
        # Collect statistics
        extraction_stats = {
            "total_sources": len(collections),
            "total_documents": 0,
            "extraction_timestamp": datetime.utcnow().isoformat(),
            "sources_breakdown": {},
            "document_types_distribution": {},
            "tier_performance": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "sample_documents": []
        }
        
        # Source mapping to tiers
        source_tiers = {
            "documents_dept_treasury": 1,
            "documents_dept_justice": 1,  
            "documents_uk_supreme_court": 2,
            "documents_aba": 5,
            "documents_new_york_bar": 5,
            "documents_texas_bar": 5
        }
        
        # Process each collection
        for collection_name in collections:
            collection = db[collection_name]
            doc_count = collection.count_documents({})
            extraction_stats["total_documents"] += doc_count
            
            # Get source name (remove 'documents_' prefix)
            source_name = collection_name.replace('documents_', '')
            extraction_stats["sources_breakdown"][source_name] = {
                "document_count": doc_count,
                "tier": source_tiers.get(collection_name, 0)
            }
            
            # Update tier performance
            tier = source_tiers.get(collection_name, 0)
            if tier in extraction_stats["tier_performance"]:
                extraction_stats["tier_performance"][tier] += doc_count
            
            # Get sample documents from this collection
            if doc_count > 0:
                sample_docs = list(collection.find().limit(2))
                for doc in sample_docs:
                    doc_type = doc.get('document_type', 'unknown')
                    extraction_stats["document_types_distribution"][doc_type] = (
                        extraction_stats["document_types_distribution"].get(doc_type, 0) + 1
                    )
                    
                    extraction_stats["sample_documents"].append({
                        "source": source_name,
                        "title": doc.get('title', 'Untitled')[:100],
                        "document_type": doc_type,
                        "content_length": doc.get('content_length', 0),
                        "confidence_score": doc.get('confidence_score', 0),
                        "content_preview": doc.get('content', '')[:300],
                        "extracted_at": doc.get('extracted_at', '').isoformat() if hasattr(doc.get('extracted_at', ''), 'isoformat') else str(doc.get('extracted_at', ''))
                    })
        
        # Load extraction report if available
        try:
            report_files = [f for f in os.listdir('/app/backend/') if f.startswith('targeted_extraction_report_') and f.endswith('.json')]
            if report_files:
                latest_report = sorted(report_files)[-1]
                with open(f'/app/backend/{latest_report}', 'r') as f:
                    extraction_report = json.load(f)
                    extraction_stats["processing_performance"] = extraction_report.get("extraction_summary", {})
                    extraction_stats["detailed_source_results"] = extraction_report.get("detailed_results", [])
        except Exception as e:
            logging.warning(f"Could not load extraction report: {e}")
        
        client.close()
        
        # Add success metrics
        extraction_stats["success_metrics"] = {
            "successful_sources": len([s for s in extraction_stats["sources_breakdown"].values() if s["document_count"] > 0]),
            "extraction_success_rate": len([s for s in extraction_stats["sources_breakdown"].values() if s["document_count"] > 0]) / max(len(collections), 1) * 100,
            "average_documents_per_source": extraction_stats["total_documents"] / max(len(collections), 1)
        }
        
        return extraction_stats
        
    except Exception as e:
        logging.error(f"Error getting extraction results: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve extraction results: {str(e)}")

@api_router.get("/extraction/documents/{source_id}")
async def get_extraction_documents(source_id: str, page: int = 1, per_page: int = 10):
    """Get documents from a specific extraction source"""
    try:
        import pymongo
        
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
        client = pymongo.MongoClient(mongo_url)
        db = client['legal_extraction_demo']
        
        collection_name = f"documents_{source_id}"
        if collection_name not in db.list_collection_names():
            raise HTTPException(status_code=404, detail=f"Source '{source_id}' not found")
        
        collection = db[collection_name]
        
        # Calculate pagination
        total_docs = collection.count_documents({})
        skip = (page - 1) * per_page
        
        # Get documents
        documents = list(collection.find({}, {'_id': 0}).skip(skip).limit(per_page))
        
        # Format datetime objects
        for doc in documents:
            if 'extracted_at' in doc and hasattr(doc['extracted_at'], 'isoformat'):
                doc['extracted_at'] = doc['extracted_at'].isoformat()
        
        client.close()
        
        return {
            "source_id": source_id,
            "total_documents": total_docs,
            "page": page, 
            "per_page": per_page,
            "total_pages": (total_docs + per_page - 1) // per_page,
            "documents": documents
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting documents for source {source_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve documents: {str(e)}")

@api_router.post("/categories", response_model=Category)
async def create_category(category_data: CategoryCreate):
    """Create a new category"""
    try:
        category = await db_service.create_category(category_data)
        return category
    except Exception as e:
        logging.error(f"Error creating category: {e}")
        raise HTTPException(status_code=500, detail="Failed to create category")

# Scraping Management Routes
@api_router.get("/scraping/config")
async def get_scraping_config():
    """Get available scraping configuration"""
    return {
        "available_categories": list(INDIABIX_CONFIG["categories"].keys()),
        "category_details": {
            name: {
                "display_name": config["display_name"],
                "subcategories": list(config["subcategories"].keys()),
                "total_target": sum(sub["target_questions"] for sub in config["subcategories"].values())
            }
            for name, config in INDIABIX_CONFIG["categories"].items()
        }
    }

@api_router.get("/scraping/jobs", response_model=List[ScrapingJob])
async def get_scraping_jobs(status: Optional[ScrapingStatus] = None):
    """Get scraping jobs with optional status filter"""
    try:
        jobs = await db_service.get_scraping_jobs(status)
        return jobs
    except Exception as e:
        logging.error(f"Error getting scraping jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve scraping jobs")

@api_router.post("/scraping/start", response_model=ScrapingStartResponse)
async def start_scraping(request: ScrapingJobRequest, background_tasks: BackgroundTasks):
    """Start a new scraping job"""
    try:
        # Validate categories
        available_categories = list(INDIABIX_CONFIG["categories"].keys())
        if request.categories:
            invalid_categories = [cat for cat in request.categories if cat not in available_categories]
            if invalid_categories:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid categories: {invalid_categories}. Available: {available_categories}"
                )
        
        # Create scraping job in database
        job_data = ScrapingJobCreate(
            job_name=request.job_name,
            target_categories=request.categories or available_categories,
            target_count=request.target_count,
            source_urls=[INDIABIX_CONFIG["base_url"]]
        )
        
        job = await db_service.create_scraping_job(job_data)
        
        # Start scraping in background
        background_tasks.add_task(run_scraping_job, job.id, job_data)
        
        # Estimate duration (rough calculation)
        estimated_minutes = (request.target_count * 0.1)  # ~0.1 minute per question
        estimated_duration = f"{int(estimated_minutes)} minutes"
        
        return ScrapingStartResponse(
            job_id=job.id,
            message="Scraping job started successfully",
            estimated_duration=estimated_duration
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error starting scraping job: {e}")
        raise HTTPException(status_code=500, detail="Failed to start scraping job")

async def run_scraping_job(job_id: str, job_data: ScrapingJobCreate):
    """Run the actual scraping job in background"""
    try:
        # Update job status to in_progress
        await db_service.update_scraping_job(
            job_id, 
            ScrapingJobUpdate(
                status=ScrapingStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            )
        )
        
        # Track active job
        active_scraping_jobs[job_id] = datetime.utcnow()
        
        # Initialize scraper
        scraper = IndiaBixScraper()
        
        # Run scraping
        result = await scraper.start_scraping(
            target_categories=job_data.target_categories,
            target_total=job_data.target_count
        )
        
        questions_data = result['questions']
        stats = result['stats']
        
        # Save questions to database
        if questions_data:
            question_ids = await db_service.create_questions_bulk(questions_data)
            
            # Update job completion
            await db_service.update_scraping_job(
                job_id,
                ScrapingJobUpdate(
                    status=ScrapingStatus.COMPLETED,
                    questions_scraped=stats['total_questions'],
                    questions_saved=len(question_ids),
                    success_rate=round((stats['success_count'] / max(stats['total_questions'], 1)) * 100, 2),
                    error_count=stats['error_count'],
                    completed_at=datetime.utcnow()
                )
            )
            
            logging.info(f"Scraping job {job_id} completed: {len(question_ids)} questions saved")
        else:
            # Update job as failed
            await db_service.update_scraping_job(
                job_id,
                ScrapingJobUpdate(
                    status=ScrapingStatus.FAILED,
                    error_count=stats.get('error_count', 1),
                    completed_at=datetime.utcnow()
                )
            )
            
            logging.error(f"Scraping job {job_id} failed: No questions extracted")
        
    except Exception as e:
        logging.error(f"Error running scraping job {job_id}: {e}")
        
        # Update job as failed
        try:
            await db_service.update_scraping_job(
                job_id,
                ScrapingJobUpdate(
                    status=ScrapingStatus.FAILED,
                    error_count=1,
                    completed_at=datetime.utcnow()
                )
            )
        except Exception as update_error:
            logging.error(f"Failed to update job status: {update_error}")
    
    finally:
        # Remove from active jobs
        active_scraping_jobs.pop(job_id, None)

@api_router.delete("/scraping/jobs/{job_id}")
async def cancel_scraping_job(job_id: str):
    """Cancel an active scraping job"""
    try:
        if job_id in active_scraping_jobs:
            # Update job status to paused/cancelled
            await db_service.update_scraping_job(
                job_id,
                ScrapingJobUpdate(
                    status=ScrapingStatus.PAUSED,
                    completed_at=datetime.utcnow()
                )
            )
            
            # Remove from active jobs
            active_scraping_jobs.pop(job_id, None)
            
            return {"message": "Scraping job cancelled successfully"}
        else:
            raise HTTPException(status_code=404, detail="Scraping job not found or not active")
    
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error cancelling scraping job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel scraping job")

# Include the router in the main app
app.include_router(api_router)

# Include ultra-scale API router if available (Step 4.1)
if ULTRA_SCALE_API_AVAILABLE:
    app.include_router(ultra_api_router, tags=["Ultra-Scale API"])
    logging.info("✅ Ultra-scale API endpoints integrated successfully")

# Include performance optimization API router if available (Step 6.1)
if PERFORMANCE_OPTIMIZATION_AVAILABLE:
    app.include_router(performance_api_router, tags=["Performance Optimization"])
    logging.info("✅ Performance optimization API endpoints integrated successfully")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
