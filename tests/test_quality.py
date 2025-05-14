import pytest
from datetime import datetime
from data_mesh.quality.engine import QualityEngine, QualityRule, QualityResult
from data_mesh.quality.monitor import QualityMonitor

@pytest.fixture
def quality_engine():
    return QualityEngine()

@pytest.fixture
def quality_monitor():
    return QualityMonitor()

@pytest.fixture
def sample_rule():
    return QualityRule(
        name="test_rule",
        description="Test rule",
        rule_type="not_null",
        parameters={},
        severity="high"
    )

def test_add_rule(quality_engine, sample_rule):
    """Test adding a quality rule."""
    quality_engine.add_rule(sample_rule)
    assert sample_rule.name in quality_engine.rules
    assert quality_engine.rules[sample_rule.name] == sample_rule

def test_remove_rule(quality_engine, sample_rule):
    """Test removing a quality rule."""
    quality_engine.add_rule(sample_rule)
    quality_engine.remove_rule(sample_rule.name)
    assert sample_rule.name not in quality_engine.rules

def test_validate_data_not_null(quality_engine, sample_rule):
    """Test not_null validation."""
    quality_engine.add_rule(sample_rule)
    
    # Test with non-null value
    results = quality_engine.validate_data("test")
    assert len(results) == 1
    assert results[0].passed
    
    # Test with null value
    results = quality_engine.validate_data(None)
    assert len(results) == 1
    assert not results[0].passed

def test_validate_data_range(quality_engine):
    """Test range validation."""
    rule = QualityRule(
        name="range_rule",
        description="Range test rule",
        rule_type="range",
        parameters={"min": 1, "max": 10},
        severity="high"
    )
    quality_engine.add_rule(rule)
    
    # Test within range
    results = quality_engine.validate_data(5)
    assert len(results) == 1
    assert results[0].passed
    
    # Test outside range
    results = quality_engine.validate_data(11)
    assert len(results) == 1
    assert not results[0].passed

def test_quality_monitor_check(quality_monitor, sample_rule):
    """Test quality monitoring."""
    quality_monitor.add_quality_rule(sample_rule)
    
    data = {
        "field1": "test",
        "field2": None
    }
    
    results = quality_monitor.check_quality(data, "test_domain")
    assert len(results) > 0
    
    # Check that metrics were updated
    report = quality_monitor.get_quality_report("test_domain")
    assert report["domain"] == "test_domain"
    assert "quality_score" in report
    assert "total_checks" in report

def test_quality_monitor_report(quality_monitor, sample_rule):
    """Test quality report generation."""
    quality_monitor.add_quality_rule(sample_rule)
    
    # Perform some checks
    data = {"field1": "test"}
    quality_monitor.check_quality(data, "test_domain")
    
    # Get report
    report = quality_monitor.get_quality_report("test_domain")
    assert isinstance(report["timestamp"], str)
    assert isinstance(report["quality_score"], float)
    assert isinstance(report["total_checks"], int)
    assert isinstance(report["check_duration"], float) 