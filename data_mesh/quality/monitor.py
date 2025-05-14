from typing import Dict, List, Optional
from datetime import datetime
import logging
from prometheus_client import Counter, Gauge, Histogram
from .engine import QualityEngine, QualityRule, QualityResult

logger = logging.getLogger(__name__)

class QualityMonitor:
    """Service for monitoring data quality and generating alerts."""
    
    def __init__(self):
        self.engine = QualityEngine()
        self._setup_metrics()
        self._setup_logging()
    
    def _setup_metrics(self):
        """Setup Prometheus metrics for monitoring."""
        self.quality_checks_total = Counter(
            'data_quality_checks_total',
            'Total number of quality checks performed',
            ['rule_name', 'result']
        )
        self.quality_check_duration = Histogram(
            'data_quality_check_duration_seconds',
            'Time spent performing quality checks',
            ['rule_name']
        )
        self.quality_score = Gauge(
            'data_quality_score',
            'Overall data quality score',
            ['domain']
        )
    
    def _setup_logging(self):
        """Configure logging for the quality monitor."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def add_quality_rule(self, rule: QualityRule) -> None:
        """Add a new quality rule to the monitor."""
        self.engine.add_rule(rule)
        logger.info(f"Added quality rule to monitor: {rule.name}")
    
    def check_quality(self, data: Dict[str, any], domain: str) -> List[QualityResult]:
        """
        Perform quality checks on the data.
        
        Args:
            data: Dictionary of data to check
            domain: Domain the data belongs to
            
        Returns:
            List of quality check results
        """
        results = []
        
        for field, value in data.items():
            # Get rules for this field
            field_rules = self._get_rules_for_field(field)
            
            for rule in field_rules:
                with self.quality_check_duration.labels(rule_name=rule.name).time():
                    result = self.engine.validate_data(value, rule.name)
                    results.extend(result)
                    
                    # Update metrics
                    self.quality_checks_total.labels(
                        rule_name=rule.name,
                        result='passed' if result[0].passed else 'failed'
                    ).inc()
        
        # Update quality score
        self._update_quality_score(domain, results)
        
        return results
    
    def _get_rules_for_field(self, field: str) -> List[QualityRule]:
        """
        Get quality rules applicable to a specific field.
        
        Args:
            field: Field name to get rules for
            
        Returns:
            List of applicable quality rules
        """
        # In a real implementation, this would filter rules based on field metadata
        # For now, return all rules
        return list(self.engine.rules.values())
    
    def _update_quality_score(self, domain: str, results: List[QualityResult]) -> None:
        """
        Update the quality score for a domain.
        
        Args:
            domain: Domain to update score for
            results: Quality check results
        """
        if not results:
            return
            
        passed_count = sum(1 for r in results if r.passed)
        total_count = len(results)
        score = (passed_count / total_count) * 100
        
        self.quality_score.labels(domain=domain).set(score)
        logger.info(f"Updated quality score for domain {domain}: {score:.2f}%")
    
    def get_quality_report(self, domain: str) -> Dict[str, any]:
        """
        Generate a quality report for a domain.
        
        Args:
            domain: Domain to generate report for
            
        Returns:
            Quality report dictionary
        """
        return {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'quality_score': self.quality_score.labels(domain=domain)._value.get(),
            'total_checks': self.quality_checks_total._value.get(),
            'check_duration': self.quality_check_duration._value.get()
        } 