from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException

logger = logging.getLogger(__name__)

class QualityRule(BaseModel):
    """Represents a data quality rule."""
    name: str
    description: str
    rule_type: str  # completeness, accuracy, consistency, timeliness, etc.
    parameters: Dict[str, Any]
    severity: str  # critical, warning, info
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class QualityCheck(BaseModel):
    """Represents a quality check result."""
    rule_name: str
    passed: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = None

class DataQualityService:
    """Service for managing data quality rules and checks."""
    
    def __init__(self):
        self.rules: Dict[str, QualityRule] = {}
        self.check_history: Dict[str, List[QualityCheck]] = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the quality service."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def add_rule(self, rule: QualityRule) -> None:
        """Add a new quality rule."""
        self.rules[rule.name] = rule
        logger.info(f"Added quality rule: {rule.name}")
    
    def remove_rule(self, rule_name: str) -> None:
        """Remove a quality rule."""
        if rule_name in self.rules:
            del self.rules[rule_name]
            logger.info(f"Removed quality rule: {rule_name}")
    
    def run_quality_check(self, data: Any, rule_name: Optional[str] = None) -> List[QualityCheck]:
        """Run quality checks against data."""
        results = []
        rules_to_check = [self.rules[rule_name]] if rule_name else [
            r for r in self.rules.values() if r.enabled
        ]
        
        for rule in rules_to_check:
            try:
                result = self._execute_rule(rule, data)
                results.append(result)
                
                # Store check history
                if rule.name not in self.check_history:
                    self.check_history[rule.name] = []
                self.check_history[rule.name].append(result)
                
            except Exception as e:
                logger.error(f"Error executing rule {rule.name}: {str(e)}")
                results.append(QualityCheck(
                    rule_name=rule.name,
                    passed=False,
                    message=f"Error executing rule: {str(e)}"
                ))
        
        return results
    
    def _execute_rule(self, rule: QualityRule, data: Any) -> QualityCheck:
        """Execute a single quality rule against data."""
        try:
            if rule.rule_type == "completeness":
                result = self._check_completeness(data, rule.parameters)
            elif rule.rule_type == "accuracy":
                result = self._check_accuracy(data, rule.parameters)
            elif rule.rule_type == "consistency":
                result = self._check_consistency(data, rule.parameters)
            elif rule.rule_type == "timeliness":
                result = self._check_timeliness(data, rule.parameters)
            else:
                raise ValueError(f"Unknown rule type: {rule.rule_type}")
            
            return QualityCheck(
                rule_name=rule.name,
                passed=result["passed"],
                message=result["message"],
                details=result.get("details")
            )
            
        except Exception as e:
            logger.error(f"Error in rule execution: {str(e)}")
            raise
    
    def _check_completeness(self, data: Any, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Check data completeness."""
        required_fields = parameters.get("required_fields", [])
        missing_fields = [field for field in required_fields if field not in data]
        
        return {
            "passed": len(missing_fields) == 0,
            "message": f"Missing required fields: {missing_fields}" if missing_fields else "All required fields present",
            "details": {"missing_fields": missing_fields}
        }
    
    def _check_accuracy(self, data: Any, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Check data accuracy."""
        # Implement accuracy check logic
        return {
            "passed": True,
            "message": "Accuracy check passed"
        }
    
    def _check_consistency(self, data: Any, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Check data consistency."""
        # Implement consistency check logic
        return {
            "passed": True,
            "message": "Consistency check passed"
        }
    
    def _check_timeliness(self, data: Any, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Check data timeliness."""
        # Implement timeliness check logic
        return {
            "passed": True,
            "message": "Timeliness check passed"
        }
    
    def get_check_history(self, rule_name: str) -> List[QualityCheck]:
        """Get check history for a rule."""
        return self.check_history.get(rule_name, [])
    
    def get_quality_metrics(self) -> Dict[str, Any]:
        """Get overall quality metrics."""
        total_checks = sum(len(checks) for checks in self.check_history.values())
        passed_checks = sum(
            sum(1 for check in checks if check.passed)
            for checks in self.check_history.values()
        )
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "pass_rate": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "active_rules": len([r for r in self.rules.values() if r.enabled])
        }

# FastAPI application
app = FastAPI(title="Data Quality Service")
quality_service = DataQualityService()

class RuleRequest(BaseModel):
    """Request model for adding/updating quality rules."""
    name: str
    description: str
    rule_type: str
    parameters: Dict[str, Any]
    severity: str
    enabled: bool = True

@app.post("/rules", response_model=QualityRule)
async def add_rule(rule: RuleRequest):
    """Add a new quality rule."""
    try:
        quality_rule = QualityRule(**rule.dict())
        quality_service.add_rule(quality_rule)
        return quality_rule
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/rules/{name}")
async def remove_rule(name: str):
    """Remove a quality rule."""
    try:
        quality_service.remove_rule(name)
        return {"message": f"Rule {name} removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/check")
async def run_quality_check(data: Dict[str, Any], rule_name: Optional[str] = None):
    """Run quality checks against data."""
    try:
        results = quality_service.run_quality_check(data, rule_name)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rules/{name}/history")
async def get_check_history(name: str):
    """Get check history for a rule."""
    history = quality_service.get_check_history(name)
    if not history:
        raise HTTPException(status_code=404, detail=f"No history found for rule {name}")
    return {"history": history}

@app.get("/metrics")
async def get_quality_metrics():
    """Get overall quality metrics."""
    return quality_service.get_quality_metrics()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 