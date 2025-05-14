from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

from ..quality.engine import QualityRule, QualityResult
from ..quality.monitor import QualityMonitor

app = FastAPI(title="Data Quality Service")
monitor = QualityMonitor()

class RuleRequest(BaseModel):
    """Request model for adding a quality rule."""
    name: str
    description: str
    rule_type: str
    parameters: Dict[str, any]
    severity: str
    enabled: bool = True

class QualityCheckRequest(BaseModel):
    """Request model for quality check."""
    data: Dict[str, any]
    domain: str

class QualityReport(BaseModel):
    """Response model for quality report."""
    domain: str
    timestamp: datetime
    quality_score: float
    total_checks: int
    check_duration: float

@app.post("/rules", response_model=QualityRule)
async def add_rule(rule: RuleRequest):
    """Add a new quality rule."""
    try:
        quality_rule = QualityRule(**rule.dict())
        monitor.add_quality_rule(quality_rule)
        return quality_rule
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/check", response_model=List[QualityResult])
async def check_quality(request: QualityCheckRequest):
    """Perform quality checks on data."""
    try:
        results = monitor.check_quality(request.data, request.domain)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/report/{domain}", response_model=QualityReport)
async def get_quality_report(domain: str):
    """Get quality report for a domain."""
    try:
        report = monitor.get_quality_report(domain)
        return QualityReport(**report)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 